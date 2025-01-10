from setuptools import setup, find_packages

setup(
    name="powermate-controller",
    version="0.1.0",
    packages=find_packages(),
    py_modules=["powermate_controller"],  # Since it's a single file
    install_requires=[
        "evdev",
    ],
    entry_points={
        'console_scripts': [
            'powermate_controller=powermate_controller:main',
        ],
    },
)