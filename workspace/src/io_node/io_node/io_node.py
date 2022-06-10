import os
import rclpy
from .submodules.manual_control import ManualControl
from .submodules.qr_menu import QRMenu
from .submodules.main_menu import MainMenu

from rclpy.node import Node

TURTLEBOT3_MODEL = os.environ["TURTLEBOT3_MODEL"]


class IONode(Node):

    def __init__(self):
        super().__init__('io_node')

        self.main_menu = MainMenu()
        self.qr_menu = QRMenu(lambda: self.load_view(self.main_menu))
        self.manual_control = ManualControl(
            lambda: self.load_view(self.main_menu)
        )

        self.main_menu.set_load_functions(
            lambda: self.load_view(self.manual_control),
            lambda: self.load_view(self.qr_menu)
        )

        self.view = self.main_menu
        self.view.open()

    def load_view(self, view):
        self.view.close()
        self.view = view
        self.view.open()


def main(args=None):
    rclpy.init(args=args)
    io_publisher = IONode()
    rclpy.spin(io_publisher)
    io_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()