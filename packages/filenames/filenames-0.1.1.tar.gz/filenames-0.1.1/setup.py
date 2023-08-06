import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='filenames',
    version='0.1.1',
    author='Teddy Katayama',
    author_email='katayama@udel.edu',
    description='Rename or Copy Files with Replacement Optinos.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kkatayama/filenames',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'filenames=filenames.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
