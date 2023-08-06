import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arvind_mission_control",
    version="0.0.4",
    author="Arvind Subramanian",
    author_email="pt.arvind@gmail.com",
    description="Mission Control Satellite Telemetry Processor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/pt-arvind/paging-mission-control",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.2",
    entry_points={"console_scripts": ["mission_control=mission_control.cli:main"]},
)
