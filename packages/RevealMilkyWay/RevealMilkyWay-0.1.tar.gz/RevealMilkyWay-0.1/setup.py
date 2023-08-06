from setuptools import setup, find_packages

setup(
    name="RevealMilkyWay",
    version=0.01,
    description=("Some frequently used functions for studying the Milky Way"),
    author='htian',
    author_email='htian_astro@163.com',
    maintainer='htian',
    maintainer_email='htian_astro@163.com',
    license='BSD License',
    packages=find_packages()
)

# python setup.py build
# python setup.py sdist
# python -m twine upload --repository pypi dist/RevealMilkyWay-0.1.tar.gz