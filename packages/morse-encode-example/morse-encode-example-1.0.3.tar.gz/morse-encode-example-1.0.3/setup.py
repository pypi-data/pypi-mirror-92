import setuptools

setuptools.setup(
    name='morse-encode-example',
    version='1.0.3',
    author="Jonny Parker",
    author_email="jonny.yatesfield@gmail.com",
    packages=["morse-encode-example"],
    license='MIT License',
    description='A very bad Morse translator.' ,
    url="https://github.com/TheMerryMango/Morse-Encryptor",
    long_description=open('README.md', encoding="utf8").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
    ]
)
