import setuptools
from os import getenv

kind = getenv("PKG_KIND")
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=f'gbwog.{kind}',  # Replace with your own username
    version=getenv("BLD_VERS"),
    author="GalB",
    author_email="gboimel98@gmail.com",
    description="DevOpsCourse Project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gboimel98/WorldOfGames/",
    packages=[f'gbwog.{kind}'],
    package_data={'': ['curr.key.sec', './.git-easy-crypt-key']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
