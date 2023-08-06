import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-mediautils',
    version='0.1.2',
    packages=find_packages(),
    include_package_data=True,
    license='GNU License',
    description='media utilities for django',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://github.com/gsteixeira/',
    author='Gustavo Selbach Teixeira',
    author_email='gsteixei@gmail.com',
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        ],
    install_requires=[
        'opencv-python>=4.2.0',
        'numpy>=1.18.0',
        'Pillow>=6.2.0',
        'python-resize-image>=1.1.19',
        ],
    package_data={
            'django-mediautils': ['mediautils/migrations/*',]
        },
)
