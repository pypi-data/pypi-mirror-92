from setuptools import setup
import versioneer

version=versioneer.get_version()
setup(
    name='signalfx-instrumentation-django',
    cmdclass=versioneer.get_cmdclass(),
    version=version,
    url='https://github.com/signalfx/python-django/',
    download_url='https://github.com/signalfx/python-django/tarball/'+version,
    license='BSD',
    author='SignalFx, Inc.',
    author_email='signalfx-oss@splunk.com',
    description='OpenTracing support for Django applications',
    long_description=open('README.rst').read(),
    packages=['django_opentracing', 'tests'],
    platforms='any',
    install_requires=[
        'django',
        'opentracing>=2.0,<2.4',
        'six',
    ],
    extras_require={
        'tests': [
            'coverage',
            'flake8<3',  # see https://github.com/zheller/flake8-quotes/issues/29
            'flake8-quotes',
            'mock',
        ],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
