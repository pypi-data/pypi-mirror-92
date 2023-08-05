import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trendalert",
    version="0.0.5",
    author="Jonathan Leon",
    author_email="jonleonaustin@gmail.com",
    description="Stock or Futures donchian breakout screener",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonleonATX/donchian_trend_alert",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
