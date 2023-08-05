from typing import List

from treehopper.api import TreehopperUsb
import usb.core
import usb.util


def find_boards() -> List[TreehopperUsb]:
    """Return a list of TreehopperUsb boards found connected to the system

    Examples:
        >>> board = find_boards()[0]  # get the first board found
    """
    boards = []
    for dev in usb.core.find(find_all=True, idVendor=0x10c4, idProduct=0x8a7e):
        boards.append(TreehopperUsb(dev))

    return boards
