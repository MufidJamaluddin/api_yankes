from setuptools import setup

setup(
    name='yankes_api',
    packages=['yankes_api'],
    include_package_data=True,
    install_requires=[
        'flask',
        'peewee',
        'lxml'
    ],
    entry_points={
        'flask.commands': [
            'migration=yankes_api.db_migrate:cli',
            'migration=yankes_api.add_initial_data:cli'
        ],
    },
)