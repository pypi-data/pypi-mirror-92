import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thinkindicator",
    version="0.1.1",
    author="Przemysław Buczkowski",
    author_email="prem@prem.moe",
    description="Tiny widget to control your ThinkPad's fan speed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/przemub/thinkindicator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Hardware"
    ],
    python_requires='>=3.6',
    scripts=['scripts/thinkindicator'],
    install_requires=['PyGObject'],
    package_data={
        "thinkindicator": ["icons/*.png"]
    }
)

