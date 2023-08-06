from setuptools import setup
setup(
    name="OS_Platform",
    version="1",
    description="Detects OS",
    long_description="This returns the OS Name in a user-friendly format etc. Android.",
    author="Pranav",
    packages=["OS_Platform"],
    entry_points={
    'console_scripts': [
        'OS_Platform=OS_Platform.OS_Platform:main',
    ],
},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)