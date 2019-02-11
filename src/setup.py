""" setup script to install coinplus solo redeem program"""
import os
from setuptools import setup, find_packages

INSTALL_REQUIRES = ["pysha3==1.0.2",
                    "scrypt==0.8.7",
                    "ecdsa==0.13",
                    "pyqt5==5.10.1",
                    ]

if os.name == 'nt':
    INSTALL_REQUIRES.append(['pywin32'])

setup(name='coinplus_solo_redeem',
      version='1.0',
      description='Redeem private key from Solo',
      author='Coinplus',
      author_email='info@coinplus.com',
      packages=find_packages(),
      install_requires=INSTALL_REQUIRES,
      package_data={
      },
      entry_points={
          'console_scripts': ['coinplus_solo_redeem = coinplus_solo_redeem.gui:main']
      }
      )
