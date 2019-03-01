import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    README = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-model-audit-history',
    version='0.1',
    packages=['audit_history'],
    include_package_data=True,
    license='MIT License',
    copyright='Copyright 2019 SmileBack, LLC',
    description='A Django model field for PostgreSQL to store changes to a model chronologically.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/nexto/django-model-audit-history',
    author='Henrik Heimbuerger',
    author_email='henrik@smileback.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
)