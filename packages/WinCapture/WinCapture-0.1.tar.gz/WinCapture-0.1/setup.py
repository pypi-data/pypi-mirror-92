from setuptools import setup

setup (
    name="WinCapture",
    version=0.1,
    author="Lightman",
    author_email="L1ghtM3n@protonmail.com",
    description="Python module to capture Desktop and Webcam",
    packages=["WinCapture"],
    install_requires=["Pillow"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
)

