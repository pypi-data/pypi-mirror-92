import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyflow_cse_asu_exp_1",
    version="1.0.0",
    author="Mahmoud Osama",
    author_email="omarashinawy@gmail.com",
    description="CSE463 Neural Networks Project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MahmoudOsama97/DL-Framework-Project",
    packages = ['pyflow_cse_asu'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)