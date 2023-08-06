import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AutoUpdate",
    version="0.0.3",
    author="BruhDev",
    author_email="mr.bruh.dev@gmail.com",
    description="Check for updates in the easiest way possible.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bruhdev.com",
    packages=setuptools.find_packages(),
    classifiers=[],
    python_requires=">=3.6",
)