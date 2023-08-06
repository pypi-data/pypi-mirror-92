import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylz78", # Replace with your own username
    entry_points= {
        'console_scripts': [
            'pylz78=pylz78:main'
        ]
    },
    version="0.1.0",
    author="Pedro Carvalho",
    author_email="ptcar@pteco.dev",
    description="lz78 compressor in python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ptcar2009/ALG2-TP1",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)