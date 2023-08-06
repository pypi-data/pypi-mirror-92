import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jvitali",
    version="0.0.1",
    author="Jean Vitali",
    author_email="vitali.jean.03@gmail.com",
    description="Displaying my first python lib, have fun using it!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JV39/jvitali",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
