import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hammer_sh", # Replace with your own username
    version="0.0.18",
    author="Sebastian Hammer",
    author_email="hammerse65450@th-nuernberg.de",
    description="A package containing useful methods for my masterthesis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hammerse65450/hammer_sh",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['sample_data/*.pickle']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pandas',
        'nltk',
        'numpy',
        'matplotlib',
        'transformers',
        'tensorflow',
        'sklearn',
        'requests',
        'bs4',
        'PyMuPDF',
        'pyocr',
        'pdf2image',
        'pdfminer.six',
        'tqdm',
        'gensim',
    ],
    python_requires='>=3.6',
)
