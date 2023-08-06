from setuptools import setup
setup(
  name = 'bmkg',
  packages = ['bmkg'],
  version = '0.0.1',
  license='MIT',
  description = 'Unofficial BMKG API Python Wrapper.',
  long_description = open('README.md', 'r', encoding='utf-8').read(),
  long_description_content_type='text/markdown',
  author = 'vierofernando',
  author_email = 'vierofernando9@gmail.com',
  url = 'https://github.com/vierofernando/bmkg',
  download_url = 'https://github.com/vierofernando/bmkg/archive/0.0.1.tar.gz',
  keywords = ['Weather', 'BMKG', 'Indonesia', 'API', 'API Wrapper', 'Wrapper'],
  install_requires=[
    'aiohttp',
    'xmltodict'
  ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
  python_requires='>=3.7',
)