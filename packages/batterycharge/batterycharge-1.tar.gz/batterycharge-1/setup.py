from setuptools import setup
setup(
    name="batterycharge",
    version="1",
    description="Gives you the battery charge",
    author="Pranav",
    packages=["batterycharge"],
    entry_points={
    'console_scripts': [
        'batterycharge=batterycharge.batterycharge:main',
    ],
},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)