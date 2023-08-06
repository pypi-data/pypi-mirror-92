from setuptools import setup, find_packages


with open('VERSION.txt') as f:
    version = f.readline()


setup(
    name='django_mxio_account_management',
    version=version,
    url='https://matix.io',
    license='MIT',
    description='Custom account management functionality for Django',
    long_description='',
    author='Connor Bode',
    author_email='connor@matix.io',
    packages=find_packages(),
	include_package_data=True,
    install_requires=[],
    zip_safe=False,
    classifiers=[],
)
