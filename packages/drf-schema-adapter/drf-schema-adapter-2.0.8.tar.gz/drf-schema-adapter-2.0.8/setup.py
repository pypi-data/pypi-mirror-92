import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drf-schema-adapter',
    version='2.0.8',
    packages=['drf_auto_endpoint', 'export_app', 'export_app.management',
              'export_app.management.commands'],
    include_package_data=True,
    license='MIT License',
    description='Making using Django with frontend libraries and frameworks DRYer',
    long_description_content_type="text/markdown",
    long_description=README,
    url='https://github.com/drf-forms/drf-schema-adapter',
    author='Emmanuelle Delescolle, Adrien Brunet, Mauro Bianchi, Mattia Larentis, Aaron Elliot Ross',
    author_email='info@levit.be',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=2.0',
        'djangorestframework>=3.8<4.0',
        'django-filter>=0.13.0',
        'Inflector>=2.0.11',
    ]
)
