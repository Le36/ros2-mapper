import os

import rclpy
from interfaces.msg import QRCode
from rclpy.node import Node
from std_msgs.msg import String

from .submodules.main_menu import MainMenu
from .submodules.manual_control import ManualControl
from .submodules.qr_menu import QRMenu

TURTLEBOT3_MODEL = os.environ["TURTLEBOT3_MODEL"]


class IONode(Node):
    def __init__(self):
        super().__init__("io_node")

        # Publishers
        self.qr_menu_publisher_ = self.create_publisher(String, "/qr_navigator", 5)
        self.main_menu_publisher_ = self.create_publisher(
            String, "/autonomous_exploration", 5
        )

        # Views
        self.main_menu = MainMenu(self.main_menu_publisher_)
        self.qr_menu = QRMenu(
            lambda: self.load_view(self.main_menu), self.qr_menu_publisher_
        )
        self.manual_control = ManualControl(lambda: self.load_view(self.main_menu))

        # Set main menu load functions
        self.main_menu.set_load_functions(
            lambda: self.load_view(self.manual_control),
            lambda: self.load_view(self.qr_menu),
        )

        # Subscriptions
        self.log_subscription_ = self.create_subscription(String, "/log", self.log, 10)
        self.qr_code_subscription_ = self.create_subscription(
            QRCode, "/qr_list", self.qr_menu.qr_listener_callback, 10
        )

        self.view = self.main_menu
        self.view.open()

    def load_view(self, view) -> None:
        self.view.close()
        self.view = view
        self.view.open()

    def log(self, msg: String) -> None:
        self.main_menu.log(msg.data)
        self.qr_menu.log(msg.data)


def main(args=None):
    """Run the node"""
    rclpy.init(args=args)
    io_publisher = IONode()
    rclpy.spin(io_publisher)
    io_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
