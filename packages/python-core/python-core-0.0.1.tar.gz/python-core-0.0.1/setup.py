
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-core", # Replace with your own username
    version="0.0.1",
    author="alexzander",
    author_email="test@gmail.com",
    description="python core package, extremely powerful and easy, created especially for lazy developers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    include_package_data=True,
    install_requires=[
        'pydub',
        'SpeechRecognition',
        'requests',
        "numpy"
    ],
    platforms="any",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)