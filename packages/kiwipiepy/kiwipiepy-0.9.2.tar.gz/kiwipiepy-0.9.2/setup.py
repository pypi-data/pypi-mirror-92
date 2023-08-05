from setuptools import setup, Extension 
from codecs import open
import os, os.path, platform
from setuptools.command.install import install

here = os.path.abspath(os.path.dirname(__file__))
exec(open('kiwipiepy/_version.py').read())

long_description = '''kiwipiepy
----------
kiwipiepy is a python version package of Kiwi(Korean Intelligent Word Identifier) which is a morphological analyzer for Korean.

https://github.com/bab2min/kiwipiepy '''

sources = []
for f in os.listdir(os.path.join(here, 'src')):
    if f.endswith('.cpp'): sources.append('src/' + f)
for f in os.listdir(os.path.join(here, 'src/core')):
    if f.endswith('.cpp'): sources.append('src/core/' + f)

largs = []
if platform.system() == 'Windows': 
    cargs = ['/O2', '/MT', '/Gy']
    largs += ['advapi32.lib']
    if os.environ.get('USE_MIMALLOC'): sources += ['mimalloc/src/static.c']
else: 
    cargs = ['-std=c++1y']
    if os.environ.get('DEBUG'): cargs += ['-O0', '-g3', '-DDEBUG']
    else: cargs += ['-O3', '-g']

if platform.system() == 'Darwin':
    cargs += ['-stdlib=libc++']
    largs += ['-stdlib=libc++']

modules = [Extension('_kiwipiepy',
    libraries=[],
    sources=sources,
    include_dirs=['mimalloc/include'],
    define_macros=[('USE_MIMALLOC', '1')] if os.environ.get('USE_MIMALLOC') else [],
    extra_compile_args=cargs, 
    extra_link_args=largs)
]

if not os.environ.get('USE_MIMALLOC'): clib = []
if platform.system() == 'Windows': clib = []
else: clib = [('mimalloc', {'sources':['mimalloc/src/static.c'], 'include_dirs':['mimalloc/include']})]

setup(
    name='kiwipiepy',
    libraries=clib,
    version=__version__,

    description='Kiwi, the Korean Tokenizer for Python',
    long_description=long_description,

    url='https://github.com/bab2min/kiwipiepy',

    author='bab2min',
    author_email='bab2min@gmail.com',

    license='LGPL v3 License',

    classifiers=[
        'Development Status :: 3 - Alpha',

        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Software Development :: Libraries",
        "Topic :: Text Processing :: Linguistic",

        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",

        'Programming Language :: Python :: 3',
        'Programming Language :: C++'
    ],

    keywords='Korean morphological analysis',
    install_requires=[
        'kiwipiepy_model==0.9.0'
    ],
    packages=['kiwipiepy'],
    include_package_data=True,
    ext_modules=modules
)
