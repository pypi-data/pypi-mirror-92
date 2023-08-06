from setuptools import setup

with open('dbcli_mongo_redis/README.txt') as inf:
    long_description = inf.read()

setup(name='dbcli_mongo_redis',
      version='0.2.1',
      description='Mongo and redis cli',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/orasul/dbcli',
      packages=['dbcli_mongo_redis.mcli', 'dbcli_mongo_redis.rcli'],
      author='Rasul Osmanov',
      install_requires=[
          'click',
          'flatten_json',
          'pymongo',
          'redis'
      ],
      entry_points={
          'console_scripts': [
              'rcli = dbcli_mongo_redis.rcli.rcli:_main',
              'mcli = dbcli_mongo_redis.mcli.mcli:_main',
          ],
      },
      include_package_data=True)