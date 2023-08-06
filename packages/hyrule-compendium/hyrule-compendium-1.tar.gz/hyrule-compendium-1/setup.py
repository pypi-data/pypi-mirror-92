import setuptools

setuptools.setup(
    name='hyrule-compendium',
    version='1',
    author='',
    author_email='',
    description='',
    long_description='''# Depreciated
    Use [this](https://github.com/gadhagod/pyrule-compendium) library.''',
    long_description_content_type='text/markdown',
    url='https://github.com/gadhagod/Hyrule-Compendium-python-client',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'pyrurle-compendium',
    ],
    python_requires='>=3.6'
)