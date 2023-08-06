import setuptools

with open("README.md",'r') as fh:
    long_description=fh.read()

setuptools.setup(
  name = 'ltspice2svg',
  include_package_data=True,
  packages = ['ltspice2svg'],
  version = '2021.04',
  license='MIT',
  description = 'Converting LTspice file to SVG',
  author = 'Harsh Agarwal',
  author_email = 'harshvinay752@gmail.com',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url = 'https://github.com/harshvinay752',
  download_url = 'https://github.com/harshvinay752/ltspice2svg/archive/2021.01.tar.gz',
  keywords = ['LTspice','spice','SVG','vector','image','convert'],
  install_requires=['svgwrite'],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
