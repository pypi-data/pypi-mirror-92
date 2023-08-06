import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dfclient",
    version="0.0.3",
    author="RBC",
    author_email="vlatish@rbc.ru",
    description="data finance client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/greyfox-dev/dfclient",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: Other/Proprietary License",
        "Operating System :: Unix",
    ],
    install_requires=['aiohttp'],
    python_requires='>=3.6.0, <4',
)
