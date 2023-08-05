from setuptools import setup

setup(
  name = 'DEL.py',
  packages=['delpy'],
  version = '0.1',
  license='MIT',
  description = 'API wrapper for discordextremelist',
  author = 'Moksej',
  author_email = 'moksej@gmail.com',
  url = 'https://github.com/discordextremelist/del.py',
  download_url = 'https://github.com/discordextremelist/del.py.git',
  install_requires=['aiohttp'],
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
)