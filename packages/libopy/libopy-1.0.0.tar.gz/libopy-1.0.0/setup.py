import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="libopy", # Replace with your own username
    version="1.0.0",
    author="@evdatsion",
    author_email="sarmad@magnusmage.com",
    description="Package for transaction offline transaction signing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evdatsion/libopy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)