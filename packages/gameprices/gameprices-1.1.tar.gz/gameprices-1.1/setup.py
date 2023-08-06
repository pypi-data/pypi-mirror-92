from setuptools import setup
long_description = open('README.rst').read()

setup(
    name='gameprices',
    packages=['gameprices', 'gameprices.shops', 'gameprices.cli', 'gameprices.test', 'gameprices.utils'],
    version='1.1',
    description='An interface for the undocumented Sony PlayStation Store PSN and Nintendo Eshop Apis',
    long_description=long_description,
    author='Matthias Kuech',
    author_email='post@matthias-kuech.de',
    url='https://github.com/snipem/psnprices',
    download_url='https://github.com/snipem/psnprices/archive/1.0.tar.gz',
    keywords=['playstation', 'eshop', 'store', 'prices'],
    license='GPL2',
    test_suite='pytest',
    entry_points={
        'console_scripts': [
            'eshopcli=gameprices.cli.cli:eshop_main',
            'psncli=gameprices.cli.cli:psn_main',
            'psndealsmailalert=gameprices.cli.psndealsmailalert:main',
            'psnmailalert=gameprices.cli.mailalert:main',
            'dealsmailalert=gameprices.cli.mailalert:main']
        }
    )
