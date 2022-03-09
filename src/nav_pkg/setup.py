from setuptools import setup

package_name = 'nav_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
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

            'helloworld_publisher = nav_pkg.helloworld_publisher:main', # temp
            'nav_arrive_subscriber = nav_pkg.nav_arrive_subscriber:main', # -> nav

            'nav_arrive_publisher = nav_pkg.nav_arrive_publisher:main', # nav ->
            'face_start_subscriber = face_pkg.face_start_subscriber:main',
        ],
    },
)
