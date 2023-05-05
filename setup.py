from setuptools import setup, find_packages

setup(
    name='src',
    version='0.1.0',
    license='MIT',
    description='A package that contains a class',
    author='Turner Luke',
    author_email='turnermluke@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'boto3',
        'botocore',
        'certifi',
        'charset-normalizer',
        'idna',
        'jmespath',
        'python-dateutil',
        'requests',
        's3transfer',
        'six',
        'urllib3',
    ],
)
