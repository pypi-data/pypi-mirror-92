import setuptools
with open("README.md", "r") as README:
    long_description = README.read()

setuptools.setup(
    name="extraEncodings",
    version="1.5.7.2",
    author="codecode",
    author_email="code80191@gmail.com",
    description="Extra text encodings and encoders.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable ',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8',
)
