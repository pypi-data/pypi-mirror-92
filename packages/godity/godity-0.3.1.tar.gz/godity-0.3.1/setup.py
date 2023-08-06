from setuptools import setup

setup(
    name = 'godity',
    version = '0.3.1',
    author = 'Samuel Andrade',
    author_email = 'sameuldeveloper45@gmail.com',
    packages = ['godity', 'godity/core', 'godity/components', 'godity/math'],
    description = 'A simple framework to create 2D games!',
    long_description = 'Godity Engine is a open-source framework based on pygame, it is being developed for to facilitate work of game developers who use pygame to create 2D games.',
    url = 'https://github.com/samueldev45/GodityEngine',
    project_urls = {
        'github': 'https://github.com/samueldev45/GodityEngine',
        'API': 'https://samueldev45.github.io/godity/docs'
    },
    license = 'MIT',
    keywords = 'game engine, framework'
)