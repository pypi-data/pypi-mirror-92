import setuptools

with open("README_PyPI.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="goldpot",
    version="0.0.3.4",
    author="Sebastian Senge",
    author_email="ssenge.public@gmail.com",
    description="A thin convenience layer on top of OpenAI's GPT-3 Python library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ssenge/Goldpot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires='>=3.7',
)
