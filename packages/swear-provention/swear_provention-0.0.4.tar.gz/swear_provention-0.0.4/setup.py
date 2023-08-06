import setuptools


with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Ethan Brammah",
    author_email="",
    name='swear_provention',
    license="MIT",
    description='a library that removes swear words from strings',
    version='v0.0.4',
    long_description=README,
    url='https://github.com/Dragon445/swear_provention',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    
    
)
