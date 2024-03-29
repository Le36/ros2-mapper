from setuptools import setup

package_name = "ros2mapper_io_node"
submodules = package_name + "/submodules"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name, submodules],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="asianomainen",
    maintainer_email="oskari.nuottonen@gmail.com",
    description="I/O node for controlling the TurtleBot3",
    license="MIT",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": ["control = ros2mapper_io_node.ros2mapper_io_node:main"],
    },
)
