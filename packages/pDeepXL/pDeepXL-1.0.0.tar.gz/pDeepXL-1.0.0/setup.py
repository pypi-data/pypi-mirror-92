import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pDeepXL",
    version="1.0.0",
    author="Zhenlin Chen",
    author_email="chenzhenlin@ict.ac.cn",
    description="MS/MS spectrum prediction for cross-linked peptide pairs by deep learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pFindStudio/pDeepXL",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)