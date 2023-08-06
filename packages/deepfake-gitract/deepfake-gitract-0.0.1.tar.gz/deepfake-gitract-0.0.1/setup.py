import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepfake-gitract", # Replace with your own username
    version="0.0.1",
    author="TBA",
    author_email="vlbthambawita@gmail.com",
    description="Deepfake gastrointestinal tract image generator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vlbthambawita/deepfake-ecg",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'deepfakeecg': ['checkpoints/g_stat.pt']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'tqdm',
        'torch',
        'pandas',
        'pathlib',
        'stylegan2_pytorch',

  ],
)