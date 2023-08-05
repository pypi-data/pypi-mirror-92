from setuptools import setup

setup(name='pycloudimage',
      version='0.1.4',
      description='Get Cloud Image from Internet',
      long_description=open('README.md',encoding="utf-8").read(),
      long_description_content_type="text/markdown",
      url='https://gitee.com/timefiles/pycloudimage',
      author='TimeStudio',
      author_email='sjgzszg@163.com',
      license='MIT',
      packages=['pycloudimage'],
      install_requires=['Pillow','pytz'])
