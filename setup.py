from setuptools import setup

setup(
    name='myDataBase',
    version='0.1.0',
    packages=['data_base_me'],
    url='',
    license='',
    author='Oliver Rudow',
    author_email='oliver.rudow@googlemail.com',
    description='basic data base class',
    install_requires=['pandas', 'file_base_me', 'auxiliary_me', 'config_me', 'tuple_me']
)
