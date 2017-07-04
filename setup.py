from setuptools import setup

setup(
    name='arithmo',
    packages=['arithmo'],
    include_package_data=True,
    install_requires=[
        'flask',
        'requests'
    ]
)
