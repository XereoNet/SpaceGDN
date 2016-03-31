from setuptools import setup, find_packages

setup(
    name='SpaceGDN',
    version='2.2.0',
    url='https://github.com/XereoNet/SpaceGDN/',
    author='Connor Peet',
    author_email='connor@connorpeet.com',
    description='Game Delivery Network for SpaceCP',
    license='AGPL-3.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Flask',
                      'Flask-Script',
                      'uwsgi',
                      'requests',
                      'beautifulsoup4',
                      'lxml',
                      'raven[flask]',
                      'pymongo']
)
