from setuptools import setup,find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='stolgo',
   version='0.1.0',
   description='Utilities for the analysis of financial data',
   license="MIT",
   long_description_content_type='text/markdown',
   long_description=long_description,
   author='stolgo Developers',
   author_email='stockalgos@gmail.com',
   project_urls={
          "Organization":"http://www.stolgo.com",
          "Source":"https://github.com/stockalgo/stolgo",
          "Tracker":"https://github.com/stockalgo/stolgo/issues"
          },
   packages=find_packages('lib'),
   package_dir = {'':'lib'},
   include_package_data=True,
   install_requires=[
            'requests',
            'pandas',
            'datetime',
            'openpyxl',
            'futures',
            'beautifulsoup4',
            'lxml'],
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',
      'Programming Language :: Python :: 3.8',
        ],
    download_url = "https://github.com/stockalgo/stolgo/archive/v0.1.0.tar.gz",
    keywords = ["candlestick-patterns-detection","price-action","algorithmic-trading-strategies",\
                "breakout-detection","algorithmic-trading-python","algo-trading-software","nasdaq-python-api","price-action-python-api"]
)