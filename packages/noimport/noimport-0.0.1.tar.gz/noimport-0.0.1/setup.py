import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="noimport", # Replace with your own username
    version="0.0.1",
    author="Andy Khang",
    author_email="andykhang404@gmail.com",
    description="A simple package to prevent the abusive use of 'import' statement in Python.",
    keywords="no import noimport suicide",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/AndyKhang404/noimport",
    py_modules=["noimport"],
    classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.4",
		"Programming Language :: Python :: 3.5",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.4',
)