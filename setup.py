from codecs import open as codecs_open
from setuptools import setup, find_packages


# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

with open('snuggs/__init__.py') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1]
            version = version.strip().strip('"')
            break

setup(name='snuggs',
      version=version,
      description=u"Snuggs are s-expressions for Numpy",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Sean Gillies",
      author_email='sean@mapbox.com',
      url='https://github.com/mapbox/snuggs',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['click', 'numpy', 'pyparsing'],
      extras_require={'test': ['pytest']})
