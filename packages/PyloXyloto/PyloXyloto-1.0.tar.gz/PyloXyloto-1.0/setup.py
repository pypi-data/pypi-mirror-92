from setuptools import setup, find_packages


def readme():
    with open("README.md") as rm:
        return rm.read()


setup(
    name='PyloXyloto',
    version='1.0',
    description='PyloXyloto is a simple Deep learning framework built from scratch with python',
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    url='https://github.com/am305949/PyloXyloto',
    download_url='',
    author='Ahmed Mohamed : AinShams University',
    author_email="myloxyloto2511@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas',
        ],
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=['DeepLearning', 'FrameWork', 'NeuralNetworks', 'TensorFlow', 'Pytorch', 'Python'],
)


