import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hitbtc-api-brunohenz",
    version="0.0.4",
    author="Bruno Henz",
    author_email="brunohzsalomao@gmail.com",
    description="Client to HitBtc API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brunohenz/hitbtc-client-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)