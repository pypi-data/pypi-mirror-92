import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DGraphics",
    version="6.4.1",
    author="Darcy Day",
    author_email="darcy.day@outlook.com",
    description="An Object Based 2D (A bit 3D) Graphics Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VertexBufferObject/DGraphics",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5, <3.8',
    keywords='development 2d graphics engine',
    install_requires=[
        "pygame",
        "pillow"
    ]
)
