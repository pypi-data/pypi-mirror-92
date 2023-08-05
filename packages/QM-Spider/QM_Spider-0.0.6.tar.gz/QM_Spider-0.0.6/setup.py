import setuptools

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="QM_Spider",
    version="0.0.6",
    author="@道长",
    author_email="ctrlf4@yeah.net",
    description="QiMai Crawler library",
    long_description="QiMai Crawler library",
    long_description_content_type="text/markdown",
    url="https://github.com/ShellMonster/QM_Spider",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)

install_requires=[
    'requests',
    'datetime'
    'pandas',
    'numpy',
    'scipy'
]

