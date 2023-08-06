import sys

# if sys.version_info < (3, 0):
#     print(sys.stderr, "{}: need Python 3, 0 or later.".format(sys.argv[0]))
#     print(sys.stderr, "Your Python is {}".format(sys.version))
#     sys.exit(1)

#with open('README.rst', 'r', encoding='utf8') as fh:
#   long_description = fh.read()

from setuptools import setup, find_packages

setup(
                 name='sjjcbCaptcha',
                 version='1.2.1',
                 description='Public POM project: sjjcbCaptcha ',
                 author='zijian',
                 license='Apache License 2.0',
                 author_email='ah.fanjian@aisino.com',
                 url='http://www.example.com',
                 packages=['sjjcbCaptcha'],
                 zip_safe=False,
                 include_package_data=True,
                 classifiers=(
                     "Programming Language :: Python :: 3",
                     "Operating System :: OS Independent"
                 )
)