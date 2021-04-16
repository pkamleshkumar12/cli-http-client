
from setuptools import setup, find_packages
from clihttpclient.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='clihttpclient',
    version=VERSION,
    description='To act as HTTP Client and Do performance test',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Kamlesh kumar',
    author_email='pkamleshkumar12@gmail.com',
    url='https://github.com/pkamleshkumar12/cli-http-client',
    license='Apache License 2.0',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'clihttpclient': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        clihttpclient = clihttpclient.main:main
    """,
)
