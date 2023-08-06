from setuptools import setup, find_packages

about = {}
with open("pensolvetools/__about__.py") as fp:
    exec(fp.read(), about)

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:  # TODO: why does this not build on circleci
    history = history_file.read()

setup(name=about['__project__'],
      version=about['__version__'],
      description="Additional functions for Pensolve's conversion from Excel to Python code",
      long_description=readme + '\n\n' + history,
      url='https://github.com/pensolve/pensolvetools',
      author=about['__author__'],
      author_email='maxim@pensolve.com',
      keywords='pensolve',
      license='MIT',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
      ],
      packages=find_packages(exclude=['contrib', 'docs', 'tests', 'examples']),
      install_requires=[
          'numpy',
                        ],
      # List additional groups of dependencies here (e.g. development
      # dependencies). You can install these using the following syntax,
      # for example:
      # $ pip install -e .[dev,test]
      extras_require={
          'test': ['pytest'],
      },
      python_requires='>=3',
      package_data={},
      zip_safe=False)


# From python packaging guides
# versioning is a 3-part MAJOR.MINOR.MAINTENANCE numbering scheme,
# where the project author increments:

# MAJOR version when they make incompatible API changes,
# MINOR version when they add functionality in a backwards-compatible manner, and
# MAINTENANCE version when they make backwards-compatible bug fixes.
