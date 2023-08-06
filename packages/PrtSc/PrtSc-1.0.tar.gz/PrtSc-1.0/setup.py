from setuptools import setup
setup(name="PrtSc",
    version="1.0",
    description="It takes a screenshot",
    author="Pranav",
    author_email="pranavcr7com@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["PrtSc"],
    include_package_data=True,
    install_requires=["pyscreenshot"],
    entry_points={
        "console_scripts": [
            "PrtSc=PrtSc:main",
        ]
    },)