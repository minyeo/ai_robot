from setuptools import setup
from setuptools import find_packages

package_name = 'face_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='piai',
    maintainer_email='piai@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'nav_arrive_publisher = nav_pkg.nav_arrive_publisher:main',
            'face_start_subscriber = face_pkg.face_start_subscriber:main',
            'face_publisher = face_pkg.face_publisher:main',
            'face_subscriber = tts_pkg.face_subscriber:main',
        ],
    },
)

