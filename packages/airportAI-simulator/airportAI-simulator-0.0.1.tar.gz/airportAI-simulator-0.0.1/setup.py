import setuptools

setuptools.setup(
    name="airportAI-simulator",
    version="0.0.1",
    author="Marek Pokropiński and Kemal Erdem",
    author_email="marek.pokropinski@outlook.com",
    description="Airport simulator",
    long_description="Airport simulator for evaluating airport gate assignment problem. Part of ariportAI project.",
    long_description_content_type="text/markdown",
    url="https://github.com/burnpiro/airport-ai",
    packages=['Simulator'],
    include_package_data=True,
    data_files=[('layout', ['Simulator/layout.json'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['numpy~=1.18.5', 'scipy', 'scikit-image', 'numba']
)