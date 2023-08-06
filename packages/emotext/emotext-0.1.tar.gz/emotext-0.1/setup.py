from setuptools import setup

def readme():
    with open("README.md", "r") as files:
        return files.read()

setup(
  name = 'emotext',
  packages = ['emotext'],
  version = '0.1',
  license='MIT',
  description = 'emotext is a python package created for analyze sentiment it can be negative, neutral or positive',
  long_description=readme(),
  long_description_content_type="text/markdown",
  author = 'Rizki Maulana',
  author_email = 'rizkimaulana348@gmail.com',
  url = 'https://github.com/rizki4106/emotext',
  download_url = 'https://github.com/rizki4106/emotext/archive/v_01.tar.gz',
  keywords = ['sentiment', 'analysis', 'machine-learning'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ]
)