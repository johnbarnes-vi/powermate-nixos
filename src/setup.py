from setuptools import setup

setup(
    name="powermate-controller",
    version="0.1.0",
    py_modules=["powermate_controller"],
    install_requires=[
        "evdev",
    ],
    entry_points={
        'console_scripts': [
            'powermate_controller=powermate_controller:main',
        ],
    },
    # Add these to handle permissions and executable bits
    options={
        'build_scripts': {
            'executable': '/usr/bin/env python3',
        },
    },
)