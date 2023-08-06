# We're linking against '../build/bin/libhumon-d.a' which is built by `../build.py`.

from setuptools import setup, Extension

with open ('README.md', 'r') as f:
      long_desc = f.read()

setup(name="humon",
      version='0.0.1',
      description='A Python wrapper over humon\'s C API, for reading Humon token streams.',
      long_description = long_desc,
      long_description_content_type = 'text/markdown',
      author='Trevor Schrock',
      author_email='spacemeat@gmail.com',
      url='https://github.com/spacemeat/humon-py',
      #package_dir={'': 'humon'},     # necessary with packages value?

      packages=["humon"],
      ext_package="humon",
      ext_modules=[Extension("humon",
                             include_dirs = ['./clib/include/humon', './clib/src'],
                             #libraries = ['humon'],
                             #library_dirs = ['./humon/build/bin'],
                             extra_compile_args = ['-ggdb3', '-O0'],
                             # TODO: include humon.h and other headers
                             sources = ["./clib/src/ansiColors.c",
                                        "./clib/src/encoding.c",
                                        "./clib/src/node.c",
                                        "./clib/src/parse.c",
                                        "./clib/src/printing.c",
                                        "./clib/src/tokenize.c",
                                        "./clib/src/trove.c",
                                        "./clib/src/utils.c",
                                        "./clib/src/vector.c",
                                        "./humon/cpkg/enumConsts.c",
                                        "./humon/cpkg/humonModule.c", 
                                        "./humon/cpkg/node-py.c",
                                        "./humon/cpkg/token-py.c",
                                        "./humon/cpkg/trove-py.c",
                                        "./humon/cpkg/utils.c"])
                   ],
      extras_require = {
            'dev': ['check-manifest', 'twine']
      }
)

#      classifiers: [todo: pypi.org/classifiers]
#      todo: readTheDocs, and MkDocs for markdown documentation
#      todo: use blessings for terminal colors?
#      todo: tox for testing different dists of python

