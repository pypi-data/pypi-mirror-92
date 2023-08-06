from setuptools import setup

version = open('VERSION').read()
setup(
    name='signalfx-instrumentation-redis',
    version=version,
    url='https://github.com/signalfx/python-redis/',
    download_url='https://github.com/signalfx/python-redis/tarball/'+version,
    license='Apache License 2.0',
    author='SignalFx, Inc.',
    author_email='signalfx-oss@splunk.com',
    description='OpenTracing support for Redis',
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    packages=['redis_opentracing'],
    platforms='any',
    install_requires=[
        'future',
        'redis',
        'opentracing>=2.0,<2.4'
    ],
    extras_require={
        'tests': [
            'flake8<3',
            'flake8-quotes',
            'mock<1.1.0',
            'pytest>=2.7,<3',
            'pytest-cov<2.6.0',
        ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
