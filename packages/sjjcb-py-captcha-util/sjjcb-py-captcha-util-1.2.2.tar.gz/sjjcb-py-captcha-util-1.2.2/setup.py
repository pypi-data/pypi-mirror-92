import sys

# if sys.version_info < (3, 0):
#     print(sys.stderr, "{}: need Python 3, 0 or later.".format(sys.argv[0]))
#     print(sys.stderr, "Your Python is {}".format(sys.version))
#     sys.exit(1)

#with open('README.rst', 'r', encoding='utf8') as fh:
#   long_description = fh.read()

from setuptools import setup, find_packages

setup(
                 name='sjjcb-py-captcha-util',
                 version='1.2.2',
                 description='Public POM project: sjjcb-py-captcha-util ',
                 author='zijian',
                 license='Apache License 2.0',
                 author_email='ah.fanjian@aisino.com',
                 url='http://www.example.com',
                 packages=['sjjcb-py-captcha-util'],
                 zip_safe=False,
                 include_package_data=True,
                 classifiers=(
                     "Programming Language :: Python :: 3",
                     "Operating System :: OS Independent",
                     "Framework :: Django"
                 )
)