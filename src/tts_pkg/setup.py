from setuptools import find_packages
from setuptools import setup

package_name = 'tts_pkg'

setup(
    name=package_name,
    version='0.0.2',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Mikael Arguedas, Pyo',
    author_email='mikael@osrfoundation.org, pyo@robotis.com',
    maintainer='Pyo',
    maintainer_email='pyo@robotis.com',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='ROS 2 rclpy basic package for the ROS 2 seminar',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # ocr
            'ocr_publisher = ocr_pkg.ocr_publisher:main',
            'tts_subscriber = tts_pkg.tts_subscriber:main',

            # nav
            'nav_arrive_publisher = face_pkg.nav_arrive_publisher:main',
            'tts_subscriber = tts_pkg.tts_subscriber:main',

            # face
            'face_publisher = face_pkg.face_publisher:main',
            'face_subscriber = tts_pkg.face_subscriber:main',


        ],
    },
)
