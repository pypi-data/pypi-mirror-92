import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="administrator",
    version="0.0.0",
    author="Trijeet Sethi",
    author_email="trijeets@gmail.com",
    description="Access to admin data APIs for inference and missing data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Trijeet/administrator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
