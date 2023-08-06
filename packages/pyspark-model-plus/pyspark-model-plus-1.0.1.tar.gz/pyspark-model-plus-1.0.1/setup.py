import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyspark-model-plus", # Replace with your own username
    version="1.0.1",
    author="Rajarshi Bhadra",
    author_email="bhadrarajarshi9@gmail.com",
    description="Enhancements to commonly used pyspark functions for building models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/RajarshiBhadra/pyspark-model-plus",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)