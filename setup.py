import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flipdotapi",
    version="0.0.2",
    author="Harper Reed",
    author_email="harper@company.lol",
    description="A class that interacts with the flipdot-server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/company-lol/flipdotapi",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
