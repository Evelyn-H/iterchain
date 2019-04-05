from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='iterchain',
    version='0.1.3',
    description='Simple and ergonomic iterator chaining for Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://iterchain.readthedocs.io/en/stable/',
    download_url='https://github.com/Evelyn-H/iterchain',
    author='Evelyn-H',
    author_email='hobert.evelyn@gmail.com',
    packages=['iterchain'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)
