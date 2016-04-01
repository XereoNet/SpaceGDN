from setuptools import setup, find_packages

setup(
    name='SpaceGDN',
    version='2.2.1',
    url='https://github.com/XereoNet/SpaceGDN/',
    author='Connor Peet',
    author_email='connor@connorpeet.com',
    description='Game Delivery Network for SpaceCP',
    license='AGPL-3.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['Flask==0.10.1',
                      'Flask-Script==2.0.5',
                      'uwsgi==2.0.12',
                      'requests==2.9.1',
                      'beautifulsoup4==4.4.1',
                      'lxml==3.6.0',
                      'raven[flask]==5.12.0',
                      'pymongo==3.2.2']
)
