import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ambibulb",
    version="0.0.4rc2",
    author="Sergey B",
    license="MIT",
    author_email="dkc.sergey.88@hotmail.com",
    description="Raspberry PI utility that controls color of your IR LED light bulb based on the dominant color of the currently played video",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bespsm/ambibulb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    setup_requires=["cffi>=1.13"],
    cffi_modules=["./snapshot_bcm/cffi_build.py:ffi"],
    install_requires=[line.strip() for line in open("./requirements.txt").readlines()],
    entry_points = {
        'console_scripts': ['ambibulb=ambibulb.__main__:main'],
    },
    python_requires=">=3.7",
)
