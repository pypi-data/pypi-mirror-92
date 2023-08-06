from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='dockit',
    version='0.1.2',
    author='Ron Chang',
    author_email='ron.hsien.chang@gmail.com',
    description=(
        'Fuzzy current location to git pull with all submodules '
        'or launch, close and exec container through docker-compose.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Ron-Chang/dockit.git',
    packages=find_packages(),
    license='MIT',
    python_requires='>=3.6',
    exclude_package_date={'':['.gitignore', 'asset', 'test', 'setup.py']},
    scripts=['bin/dockit'],
)
