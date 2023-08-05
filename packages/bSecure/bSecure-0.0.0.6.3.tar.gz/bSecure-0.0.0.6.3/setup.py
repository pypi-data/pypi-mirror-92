import pathlib

from setuptools import setup, find_packages

VERSION = '0.0.0.6.3'
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="bSecure",
    version=VERSION,
    description="bSecure is a Universal Checkout for Pakistan (Alpha Release)",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://bsecure.pk",
    author="bSecure",
    author_email="tech@bsecure.pk",
    license="MIT",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
