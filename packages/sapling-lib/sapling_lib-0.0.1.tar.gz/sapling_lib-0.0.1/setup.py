from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8'
]


setup(
    name='sapling_lib',
    version='0.0.1',
    description='Collection of sapling API functions, simplified',
    long_description=open('README.md').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    url='',
    author='Sunny Shahi',
    author_email='shahisunny.990@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='Sapling, api',
    packages=find_packages(),
    install_requires=['requests']
)
