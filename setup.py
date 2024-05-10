from setuptools import setup, find_packages


def get_version() -> str:
    with open('pyenigma/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip("'").strip("v")
    raise ValueError("Version not found")


setup(
    name='pyenigma',
    version=get_version(),
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pyenigma=pyenigma.cli:main',
        ],
    },
    install_requires=[],
    python_requires='>=3.6',
)
