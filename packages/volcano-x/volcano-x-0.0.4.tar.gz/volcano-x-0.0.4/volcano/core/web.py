#!/usr/bin/python3

import json
import os.path

from twisted.web.resource import Resource, NoResource
from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.util import redirectTo
from twisted.internet.error import CannotListenError

from ..lib.xml_reader import LoadException
from ..lib.stddef import ValueType


def configure_web_args(parser):
    parser.add_argument('--web_iface', help='Web listen interface', default='')  # twisted.listenTcp (..iface='') defaults to all
    parser.add_argument('--web_port', help='Web tcp port', default=0, type=int)
    parser.add_argument('--web_ctrl', help='Enable remote control over web', action='store_true')


class WebException(Exception):
    def __init__(self, message, http_code=400):
        super().__init__(message)
        self.http_code = http_code


class Args:     # pylint: disable=too-few-public-methods
    def __init__(self, req):
        self.req_ = req

    def get_str(self, name, default=None):
        val = self.req_.args.get(name.encode('utf-8'), None)
        if val is None or not val:  # val is none or list[]
            if default is None:
                raise WebException('Missing "{}" argument'.format(name), 400)
            return default

        assert isinstance(val, list)
        return val[0].decode('utf-8')


class VolcanoJsonService(Resource):
    isLeaf = True
    Database = None

    def get_json(self, request):
        pass

    def render_GET(self, request):
        try:
            res = self.get_json(request)    # pylint: disable=assignment-from-no-return
        except WebException as ex:  # other exceptions produce html page with call stack
            request.setHeader(b'content-type', b'text/plain')
            request.setResponseCode(ex.http_code)
            return str(ex).encode('utf-8')

        request.setHeader(b'content-type', b'application/json')
        return json.dumps(res).encode('utf-8')


class CmdInfo(VolcanoJsonService):
    def get_json(self, request):
        return {
            "version": {
                "major": 1,
                "minor": 1,
                "patch": 1,
            },
            "web": {
                "ctrl": g_env.web_ctrl,
                "remoteStop": False,
            }
        }


class CmdLs(VolcanoJsonService):
    def get_json(self, request):
        db = VolcanoJsonService.Database
        assert db
        
        args = Args(request)
        tag_name = args.get_str('tag', '')  # throws WebException
        tags_list = None
        if not tag_name:  # list root
            tags_list = db.enum_root_tags()
        else:
            tag = db.find_tag_by_name(tag_name)
            if not tag:
                raise WebException('Tag "{}" not found'.format(tag_name), 400)
            tags_list = tag.enum_child_tags()
        return list(map(lambda x: x.short_name(), tags_list))


class CmdStat(VolcanoJsonService):
    def get_json(self, request):
        db = VolcanoJsonService.Database
        assert db

        args = Args(request)

        tag_name = args.get_str('tag')  # throws WebException
        data = args.get_str('d', '')

        tag = db.find_tag_by_name(tag_name)
        if not tag:
            raise WebException('Tag "{}" not found'.format(tag_name), 400)

        res = {}

        # title, eu, id, children, parents
        if 't' in data:
            res['type'] = tag.var().type_str()
        if 'T' in data:
            res['title'] = tag.attributes.get('title', '')
        if 'n' in data:
            res['name'] = tag.short_name()
        if 'N' in data:
            res['fullName'] = tag.full_name()
        if 'c' in data:
            res['hasChildren'] = tag.has_children()  # pylint: disable=len-as-condition

        return res


class CmdRead(VolcanoJsonService):
    def get_json(self, request):
        db = VolcanoJsonService.Database
        assert db
    
        args = Args(request)

        tag_name = args.get_str('tag')  # throws WebException
        tag = db.find_tag_by_name(tag_name)

        if not tag:
            raise WebException('Tag "{}" not found'.format(tag_name), 400)

        if tag.var().is_void():
            raise WebException('Tag "{}" is VOID'.format(tag_name), 400)

        return {
            'v': tag.var().get_value(),
            'q': tag.quality,
            #'t': '{}Z'.format(tag.tstamp.isoformat(timespec='milliseconds')) if tag.tstamp else None,
            # isoformat with timespec is Python 3.6
            't': (tag.tstamp_utc.isoformat() + 'Z') if tag.tstamp_utc else None,
        }
        
        
class CmdWrite(VolcanoJsonService):
    isLeaf = True
    
    def render_GET(self, request):
        '''
            На данный момент управление возможно через GET по следующим причинам:
                - удобно тестировать через браузер
                - сама по себе фича все равно отладочная
        '''
        #request.setHeader(b'content-type', b'text/plain')
        #request.setResponseCode(400)
        #return 'Use POST to set '.encode('utf-8')
        return self.render_POST(request)

    def render_POST(self, request):  # pylint: disable=no-self-use
        db = VolcanoJsonService.Database
        assert db
        
        try:
            args = Args(request)    # !WebException
            
            tag_name = args.get_str('tag')  # !WebException
            tag_val = args.get_str('val')  # !WebException
            tag = db.find_tag_by_name(tag_name)

            if not tag:
                raise WebException('Tag "{}" not found'.format(tag_name), 404)

            # env.web_ctrl is not checked because otherwise CmdWrite handler wont be added

            # Convert value
            proper_value = None     # pylint: disable=unused-variable
            if tag.var().vt() == ValueType.VT_BOOL:
                if tag_val == '1':
                    proper_value = True
                elif tag_val == '0':
                    proper_value = False
                else:
                    raise WebException('Cant convert value "{}" to type {} of tag "{}". Use "1" and "0"'.format(tag_val, tag.var().vt(), tag_name), 400)
            elif tag.var().vt() == ValueType.VT_INT:
                try:
                    proper_value = int(tag_val)
                except ValueError:
                    raise WebException('Cant convert value "{}" to type {} of tag "{}"'.format(tag_val, tag.var().vt(), tag_name), 400)
            elif tag.var().vt() == ValueType.VT_FLOAT:
                try:
                    proper_value = float(tag_val)
                except ValueError:
                    raise WebException('Cant convert value "{}" to type {} of tag "{}"'.format(tag_val, tag.var().vt(), tag_name), 400)
            elif tag.var().vt() == ValueType.VT_STR:
                proper_value = tag_val
            else:
                raise WebException('Tag "{}" is VOID'.format(tag_name), 400)
            
            # !!!! MyLavaClient.Inst.set_tag(tag_name, proper_value)
            
            request.setHeader(b'content-type', b'text/plain')
            return 'OK'.encode('utf-8')
            
        except WebException as ex:  # other exceptions produce html page with call stack
            request.setHeader(b'content-type', b'text/plain')
            request.setResponseCode(ex.http_code)
            return str(ex).encode('utf-8')


class IndexResource(Resource):
    def render_GET(self, request):  # pylint: disable=no-self-use
        return redirectTo(b'/www/index.html', request)


class FaviconResource(Resource):
    def render_GET(self, request):  # pylint: disable=no-self-use
        return redirectTo(b'/www/favicon.ico', request)


class MyWebRoot(Resource):
    index = IndexResource()
    favicon = FaviconResource()

    def getChild(self, path, request):
        if g_env.www and path in (b'', b'index.html'):
            return self.index

        if g_env.www and (path == b'favicon.ico'):
            return self.favicon

        resp = Resource.getChild(self, path, request)
        if isinstance(resp, NoResource):
            g_log.warning('Not found %s', path)
        return resp

g_env = None
g_log = None

def init_web(env, db, reactor, log):
    global g_env    # pylint: disable=global-statement
    g_env = env
    
    global g_log    # pylint: disable=global-statement
    g_log = log
    
    if env.web_port == 0:
        return
    
    my_path = os.path.dirname(__file__)
    assert my_path
    env.www = my_path + '/www'

    if os.path.isdir(env.www):
        g_log.info('Default www path is used: %s', env.www)
    else:
        g_log.error('Default www path not found: %s', env.www)

    g_log.info('Remote control is %s', 'ON' if env.web_ctrl else 'OFF')
    
    VolcanoJsonService.Database = db
    g_http_factory = None

    try:
        root = MyWebRoot()

        if env.www:
            root.putChild(b'www', File(env.www))

        root.putChild(b'info.json', CmdInfo())
        root.putChild(b'ls.json', CmdLs())
        root.putChild(b'stat.json', CmdStat())
        root.putChild(b'read.json', CmdRead())
        
        if env.web_ctrl:
            root.putChild(b'set', CmdWrite())

        g_http_factory = Site(root)
        log.info('Start web interface: iface=%s port=%s', env.web_iface, env.web_port)
        try:
            reactor.listenTCP(env.web_port, g_http_factory, interface=env.web_iface)    # pylint: disable=no-member
        except CannotListenError as ex:
            log.error(ex)
            reactor.stop()  # pylint: disable=no-member

    except (LoadException, Warning) as ex:
        log.error(ex)
