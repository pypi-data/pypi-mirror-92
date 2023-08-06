import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = []
for package in setuptools.find_packages():
    if not package.startswith("tests"):
        packages.append(package)

setuptools.setup(
    name="gcloud-functions-utils",
    version="0.6.0",
    author="Johan Niklasson",
    author_email="johan@niklasson.me",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vonNiklasson/gcloud-functions-utils",
    packages=packages,
    install_requires=[],
    extras_require={
        'test-tools': [
            "functions-framework==2.1.0",
            "requests==2.25.1"
        ]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)
