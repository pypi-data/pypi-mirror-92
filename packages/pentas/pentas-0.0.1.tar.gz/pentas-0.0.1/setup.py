from setuptools import setup

setup(
    name='pentas',
    version='0.0.1',
    url='https://github.com/caiocarneloz/pentas',
    license='MIT License',
    author='Caio Carneloz',
    author_email='caiocarneloz@gmail.com',
    keywords='plotting',
    description=u'Simple functions for plotting relevant informations',
    packages=['pentas'],
    install_requires=['pandas', 'numpy', 'matplotlib'],
)