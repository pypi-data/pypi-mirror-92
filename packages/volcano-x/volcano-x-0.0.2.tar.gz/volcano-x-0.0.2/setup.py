from setuptools import setup

with open('requirements.txt') as f:
    requires = list(filter(lambda x: not not x, map(lambda x: x.strip(), f.readlines())))

with open('version.txt') as f:
    ver = f.read().strip()

setup(
    name='volcano-x',
    version=ver,
    description='VolcanoX on Python',
    author='Vinogradov D',
    author_email='dgrapes@gmail.com',
    license='MIT',
    packages=['volcano.core', 'volcano.poller', 'volcano.web', 'volcano.mbsrv', 'volcano.lib', 'volcano.twistedclient'],
    package_data={'': ['demo.xml']},
    zip_safe=False,
    install_requires=requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
