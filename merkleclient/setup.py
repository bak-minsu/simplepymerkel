import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-pkg-YOUR-USERNAME-HERE", # Replace with your own username
    version="0.1.0",
    author="Min Su Park",
    author_email="minsupark@live.com",
    description="A naive Merkle Tree Implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bak-minsu/simplepymerkletree",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)