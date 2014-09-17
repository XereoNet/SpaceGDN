from setuptools import setup, find_packages

setup(
    name='SpaceGDN',
    version='2.1.2',
    url='https://github.com/connor4312/querytree',
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