import event,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

desc="{} Author:{}".format(
    event.__doc__.replace('\n',''),event.__author__)
try:
    long_desc=event.__doc__+open("README.rst").read()
except OSError:
    long_desc=desc

setup(
  name='event-simulate',
  version=event.__version__,
  description=desc,
  long_description=long_desc,
  author=event.__author__,
  author_email=event.__email__,
  platform="win32",
  packages=['event'],
  keywords=["simulate","key","mouse","event","键盘","鼠标"],
  classifiers=[
      'Programming Language :: Python',
      "Natural Language :: Chinese (Simplified)"],
)
