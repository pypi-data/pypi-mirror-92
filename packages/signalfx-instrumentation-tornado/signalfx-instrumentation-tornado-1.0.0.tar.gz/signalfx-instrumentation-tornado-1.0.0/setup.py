from setuptools import setup

version = open('VERSION').read()
setup(
    name='signalfx-instrumentation-tornado',
    version=version,
    url='https://github.com/signalfx/python-tornado/',
    download_url='https://github.com/signalfx/python-tornado/tarball/'+version,
    license='Apache License 2.0',
    author='SignalFx, Inc.',
    author_email='signalfx-oss@splunk.com',
    description='OpenTracing support for Tornado applications',
    long_description=open('README.rst').read(),
    packages=['tornado_opentracing'],
    platforms='any',
    install_requires=[
        'tornado',
        'opentracing>=2.1,<2.4',
        'wrapt',
    ],
    extras_require={
        'tests': [
            'flake8<4',
            'flake8-quotes',
            'pytest>=4.6.9',
            'pytest-cov',
            'mock',
            'tox',
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
