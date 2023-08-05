from setuptools import setup, find_packages

setup(name='dbcli_mongo_redis',
      version='0.1.3',
      description='Mongo and redis cli',
      url='https://github.com/orasul/dbcli',
      packages=['dbcli_mongo_redis.mcli', 'dbcli_mongo_redis.rcli'],
      author='Rasul Osmanov',
      install_requires=[
          'click',
          'flatten_json',
          'pymongo',
          'bson',
          'redis'
      ],
      include_package_data=True)