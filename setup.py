# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faster_grad_cam', 'faster_grad_cam.01_float32']

package_data = \
{'': ['*'],
 'faster_grad_cam': ['02_weight_quantization/*',
                     '03_integer_quantization/*',
                     'model/*']}

install_requires = \
['numpy==1.23',
 'opencv-python>=4.7.0.68,<5.0.0.0',
 'scikit-learn==0.22',
 'tensorflow>=2.11.0,<3.0.0']

entry_points = \
{'console_scripts': ['faster_grad_cam = faster_grad_cam.demo:run']}

setup_kwargs = {
    'name': 'faster-grad-cam',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'guozhenyu2zj',
    'author_email': 'guozhenyu2zj@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
