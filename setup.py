# setup.py
from setuptools import setup, find_packages

setup(
    name='my_package',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        # e.g., 'numpy', 'requests'
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A brief description of your package',
    url='https://github.com/yourusername/my_package',  # Optional
)