from setuptools import setup

package_name = "ros2mapper_explore_node"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="suonpaas",
    maintainer_email="sami.suonpaa@gmail.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "launch = ros2mapper_explore_node.ros2mapper_explore_node:main"
        ],
    },
)
