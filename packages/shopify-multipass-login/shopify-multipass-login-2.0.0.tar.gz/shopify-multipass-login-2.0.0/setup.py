from setuptools import setup

setup(
    name='shopify-multipass-login',
    version='2.0.0',
    description='Shopify Multipass module for Python',
    url='https://github.com/dylantack/shopify-multipass',
    author='dylantack',
    license='Apache 2.0 License',
    packages=['multipass'],
    install_requires=['M2Crypto>=0.35.2'],
)
