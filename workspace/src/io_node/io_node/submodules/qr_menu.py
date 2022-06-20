import os
import select
import sys
import termios
import threading
import tty
from typing import List

from interfaces.msg import QRCode
from std_msgs.msg import String

TURTLEBOT3_MODEL = os.environ["TURTLEBOT3_MODEL"]

QR_MENU = """
List of observed QR codes
---------------------------
%s
---------------------------
1-9 : navigate to a found QR code
0 : stop navigation

m : return to main menu

CTRL-C to quit
---------------------------

"""


class QRMenu:
    def __init__(self, return_to_menu, publisher) -> None:
        self._return_to_menu = return_to_menu
        self._publisher = publisher
        self._running = False
        self._data_to_log = None
        self._reprint_menu = False
        self._qr_codes: List[QRCode] = []

    def open(self) -> None:
        self._running = True
        self._main()

    def close(self) -> None:
        self._running = False

    def log(self, data: str) -> None:
        if self._running:
            self._data_to_log = data

    def qr_listener_callback(self, qr_code: QRCode) -> None:
        """Listen for QR codes being found and add them to QR menu list"""
        for local_qr_code in self._qr_codes:
            if qr_code.id == local_qr_code.id:
                return

        self._qr_codes.append(qr_code)
        if self._running:
            self._reprint_menu = True

    def _qr_navigation_callback(self, msg_command: String) -> None:
        """Publish user input for QR code id"""
        self._publisher.publish(String(data=msg_command))

    def _get_key(self, settings):
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ""

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def _print_menu(self):
        os.system("clear")
        if self._qr_codes:
            formatted_list = [
                f"{i+1}: '{qr_code.id}'" for i, qr_code in enumerate(self._qr_codes)
            ]
            print(QR_MENU % "\n".join(formatted_list))
        else:
            print(QR_MENU % "No QR codes found")

    def _handle_input(self):
        settings = termios.tcgetattr(sys.stdin)

        while self._running:
            key = self._get_key(settings)
            if self._reprint_menu:
                self._print_menu()
                self._reprint_menu = False
            if self._data_to_log:
                print(self._data_to_log)
                self._data_to_log = None

            if key == "\x03":
                exit(0)
            elif key.isdigit():
                index = int(key)
                if index < 0 or index > 9:
                    self._print_menu()
                    print("QR code index error. Please input a number between 1-9.")
                elif index == 0:
                    self._qr_navigation_callback("0")
                    self._print_menu()
                    print("Navigation stopped")
                else:
                    self._qr_navigation_callback(str(index))
                    self._print_menu()
                    print("Navigating to", index)
            elif key == "m":
                self._return_to_menu()
            elif key:
                self._print_menu()
                print("Input not recognized")

    def _main(self):
        self._print_menu()

        self.thread = threading.Thread(target=self._handle_input)
        self.thread.start()
