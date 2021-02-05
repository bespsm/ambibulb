import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ambibulb",
    version="0.0.4",
    author="Sergey B",
    license="MIT",
    author_email="dkc.sergey.88@hotmail.com",
    description="Raspberry PI utility that controls color of your IR LED light bulb based on the dominant color of the currently played video",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bespsm/ambibulb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Utilities",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
    ],
    setup_requires=["cffi>=1.13"],
    cffi_modules=["./snapshot_bcm/cffi_build.py:ffi"],
    install_requires=[
        line.strip() for line in open("./requirements.txt").readlines()
    ],
    entry_points={
        "console_scripts": ["ambibulb=ambibulb.__main__:main"],
    },
    platforms='linux',
    python_requires=">=3.7",
)
