import setuptools

with open("README.md","r",encoding="utf-8") as f:
    long_description=f.read()

setuptools.setup(name="slbb_armstr",version="0.0.1",author="bavishyaa",author_email="bavishyaa@armstrong.com",
    description="A Armstrong no. code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bavishyaa/Python-Capsule/Package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
