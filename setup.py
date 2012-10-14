import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ["sqlalchemy==0.7.9",
            "pillow==1.7.7,"
    ]

setup(name='onfo.octavius',
      version='0.1',
      description='simple file asset management',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web tools',
      package_dir={'':'src'},
      packages=find_packages("src"),
      include_package_data=True,
      zip_safe=False,
      test_suite='tests',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      """,
      namespace_packages= ['onfo'],
      )

