from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='xls-to-csv',
    version='1.0.0',
    description='XLS to CSV converter. Complementary to xlsx2csv package',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Miroslav Isikiyski',
    author_email='misho8520@abv.bg',
    keywords=['xls', 'csv', 'convert', 'python', 'pandas', 'xlrd'],
    url='https://github.com/Sosomqk/xlstocsv',
    download_url='https://pypi.org/project/xls-to-csv/'
)

install_requires = [
    'elasticsearch>=6.0.0,<7.0.0',
    'jinja2'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)