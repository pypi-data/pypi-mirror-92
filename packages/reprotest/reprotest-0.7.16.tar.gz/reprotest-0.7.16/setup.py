#!/usr/bin/env python3

# Licensed under the GPL: https://www.gnu.org/licenses/gpl-3.0.en.html
# For details: reprotest/debian/copyright

from setuptools import setup, find_packages

setup(name='reprotest',
      version='0.7.16',
      description='Build packages and check them for reproducibility.',
      long_description=open('README.rst', encoding='utf-8').read(),
      author='Ximin Luo, Ceridwen',
      author_email='infinity0@debian.org, ceridwenv@gmail.com',
      license='GPL-3+',
      url='https://salsa.debian.org/reproducible-builds/reprotest',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'reprotest = reprotest:main'
              ],
          },
      install_requires=[
          'diffoscope',
          'rstr',
          'distro',
          ],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Topic :: Utilities',
          ],
      zip_safe=False,
      include_package_data=True
      )
