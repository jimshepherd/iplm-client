from setuptools import setup

setup(
    name='iplm_client',
    version='0.1',
    packages=['iplm_client'],
    url='',
    license='MIT',
    author='Jim Shepherd',
    author_email='jim@cove.co',
    description='IPLM python client',
    python_requires='>=3.6',
    install_requires=[
        'gql[aiohttp]',  # GraphQL utilities
    ],
    extras_require={
        'test': [
            'coverage',
            'mixer',
        ],
    },
)
