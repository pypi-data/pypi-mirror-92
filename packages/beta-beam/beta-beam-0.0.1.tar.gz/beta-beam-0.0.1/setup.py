import setuptools

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="beta-beam", # Replace with your own username
    version="0.0.1",
    author="patod01",
    author_email="patod01@telegmail.com",
    license='WTFPL',
    description="My last hope to get a degree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patod01/beta-beam",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    install_requires=['Pillow'],
    python_requires='>=3.9',
)
