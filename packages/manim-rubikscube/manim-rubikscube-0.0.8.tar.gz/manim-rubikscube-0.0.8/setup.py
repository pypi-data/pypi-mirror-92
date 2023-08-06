# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_rubikscube', 'manim_rubikscube.kociemba']

package_data = \
{'': ['*'], 'manim_rubikscube.kociemba': ['tables/*']}

install_requires = \
['manim']

entry_points = \
{'manim.plugins': ['manim_rubikscube = manim_rubikscube']}

setup_kwargs = {
    'name': 'manim-rubikscube',
    'version': '0.0.8',
    'description': "A Manim implementation of a Rubik's Cube",
    'long_description': 'Manim RubiksCube\n----------------\nFor installation, importing, use, examples, and more `see the Github repository <https://github.com/WampyCakes/manim-rubikscube>`_.',
    'author': 'KingWampy',
    'author_email': 'none@ya.business',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/WampyCakes/manim-rubikscube',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
