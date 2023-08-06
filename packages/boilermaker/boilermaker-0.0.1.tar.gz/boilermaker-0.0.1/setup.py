# We're linking against '../build/bin/libhumon-d.a' which is built by `../build.py`.

from setuptools import setup

with open ('README.md', 'r') as f:
      long_desc = f.read()

setup(name="boilermaker",
      version='0.0.1',
      description='A C++ code generator that transforms a declarative description into static types.',
      long_description = long_desc,
      long_description_content_type = 'text/markdown',
      author='Trevor Schrock',
      author_email='spacemeat@gmail.com',
      url='https://github.com/spacemeat/boilermaker',

      packages=["boilermaker"],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: C++",
            "Topic :: Software Development :: Code Generators"
      ],
      install_requires = [
          'humon',
          'pygccxml>=2.0.1'
      ],
      extras_require = {
            'dev': ['check-manifest', 'twine']
      },
      python_requires='>=3.8'
)
