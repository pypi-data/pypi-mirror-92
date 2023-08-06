import setuptools

with open("./src/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ccdl", 
    version="0.1.11",
    author="vircoys",
    author_email="vircoys@gmail.com",
    description="Online comic downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vircoys/ccdl",
    license="unlicense",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Public Domain",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "lxml",
        "numpy",
        "Pillow",
        "requests",
        "selenium",
        "pyexecjs"
    ]
)