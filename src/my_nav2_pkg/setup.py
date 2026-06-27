from setuptools import setup
from glob import glob
import os

package_name = 'my_nav2_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),

        ('share/' + package_name, ['package.xml']),


        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),


        (os.path.join('share', package_name, 'maps'),
            glob('maps/*')),


        (os.path.join('share', package_name, 'config'),
            glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='japleen',
    maintainer_email='kjapleen516@gmail.com',
    description='Nav2 patrol package',
    license='TODO',
    entry_points={
        'console_scripts': [
            'patrol_node = my_nav2_pkg.patrol_node:main',
            'vision_node = my_nav2_pkg.vision_node:main',
        ],
    },
)
