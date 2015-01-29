#####################################################################################
#
# To build the package and upload to PyPi
#    python setup.py sdist upload 
#
# To build and upload to Test PyPi
#    python setup.py sdist upload -r https://testpypi.python.org/pypi
#
#####################################################################################

from distutils.core import setup
setup(
    name = 'egautotest',
    packages = ['egautotest', 'egautotest.loggers'], # this must be the same as the name above
    scripts = ['test_runner.py'],
    version = '0.1.11',
    description = 'An automated testing toolkit',
    author = 'E-gineering LLC',
    author_email = 'eg.pypi@e-gineering.com', # contact email
    url = '', # url with information about the package
    download_url = 'https://bitbucket.org/e-gineering/e-g_automated_testing_poc/get/tag/0.1.tar.gz', # should be a url of the tarball
    keywords = ['testing', 'automated testing', 'functional testing'], # arbitrary keywords
    classifiers = [],
)
