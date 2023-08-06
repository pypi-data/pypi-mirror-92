# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()
long_desc = "Wikidict parser package"

with open('LICENSE') as f:
    license = f.read()

setup(
    name='wikidictparser',
    version='1.4',
    # description='Sample package for Python-Guide.org',
    
    description = long_desc,
    author='Lukasz Sliwinski',
    author_email='luki3141@gmail.com',
    url='https://github.com/ls2716/wikidictparser_package',
    # long_description=readme,
    # long_description_content_type="text/markdown",
    license=license,
    install_requires=[
          'requests',
          'bs4',
          'pandas',
          'lxml',
      ],
    packages=find_packages(exclude=('tests', 'docs')),
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ]
)

