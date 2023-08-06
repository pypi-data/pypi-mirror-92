import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybungie",
    version="0.5.8",
    author="Hayden Cole",
    author_email="cole.haydenj@gmail.com",
    description="For interacting with the Bungie.net API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hayden-J-C/pybungie.git",
    packages=['pybungie'],
    package_data={'pybungie': ['config/*', ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests', 'pyOpenSSL', 'python-dotenv'],
    python_requires='>=3.6',
)
