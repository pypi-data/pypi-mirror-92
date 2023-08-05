from setuptools import setup, find_packages

setup(name='dbcli_mongo_redis',
      version='0.1.2',
      description='mcli & rcli.',
      long_description='Mongo cli and redis cli.',
      url='https://github.com/orasul/dbcli',
      packages=['dbcli_mongo_redis.mcli', 'dbcli_mongo_redis.rcli'],
      install_requires=[
          'click',
          'flatten_json',
          'pymongo',
          'bson',
          'redis'
      ],
      include_package_data=True)