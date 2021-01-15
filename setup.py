import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ambibulb",
    version="0.0.3",
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
    install_requires=[
        "joblib>=1.0.0",
        "numpy>=1.19.4",
        "Pillow>=8.0.1",
        "scikit-learn>=0.23.2",
        "scipy>=1.6.0",
        "threadpoolctl>=2.1.0"
      ],
    python_requires=">=3.7",
)
