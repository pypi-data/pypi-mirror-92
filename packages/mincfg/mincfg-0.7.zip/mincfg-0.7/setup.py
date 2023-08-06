import itertools

# bootstrap if we need to
try:
        import setuptools  # noqa
except ImportError:
        from ez_setup import use_setuptools
        use_setuptools()

from setuptools import setup, find_packages

classifiers = [ 'Development Status :: 5 - Production/Stable'
              , 'Environment :: Console'
              , 'Intended Audience :: Developers'
              , 'Intended Audience :: System Administrators'
              , 'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
              , 'Natural Language :: English'
              , 'Operating System :: MacOS :: MacOS X'
              , 'Operating System :: Microsoft :: Windows'
              , 'Operating System :: POSIX'
              , 'Programming Language :: Python :: 3.7'
              , 'Programming Language :: Python :: Implementation :: CPython'
              ]

extras = {
    'yaml': ['pyyaml'],
    'ini': ['configobj'],
    'env': ['python-dotenv'],
}
extras['all'] = list(itertools.chain.from_iterable(extras.values()))
doc_build_deps = [ 'sphinx', 'furo' ]
extras['dev'] = ['pytest', 'pytest-cov', 'pytest-pylint', 'pytest-mypy', 'wheel' ] + extras['all'] + doc_build_deps

setup(  author = 'Paul Jimenez'
      , author_email = 'pj@place.org'
      , classifiers = classifiers
      , description = 'Minimal Application Configuration'
      , name = 'mincfg'
      , url = 'http://github.com/pjz/mincfg'
      , packages = find_packages()
      , version = '0.7'
      , install_requires = [ ]
      , extras_require = extras
      , zip_safe = False
     )

