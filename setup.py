"""
Setup for the Rise Garden API package.
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="risegardenapi-chimerasaurus", # Replace with your own username
    version="0.0.9",
    author="James Malone",
    author_email="me@jamalone.com",
    description="Interact with the Rise Garden API from Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chimerasaurus/rise-garden-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
