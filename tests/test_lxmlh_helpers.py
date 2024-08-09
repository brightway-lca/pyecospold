"""Test cases for the __helpers__ module."""

from lxml import etree
from pyecospold.lxmlh import fill_in_defaults


def test_create_attribute(ship_order: etree.ElementTree) -> None:
    """It creates an attribute that user can get and set properly."""
    assert ship_order.orderId == "889923"

    newOrderId = "1234"
    ship_order.orderId = newOrderId
    assert ship_order.orderId == newOrderId


def test_create_element_text(ship_order: etree.ElementTree) -> None:
    """It creates an element text that user can get and set properly."""
    assert ship_order.orderPerson == "John Smith"

    newOrderPerson = "John Doe"
    ship_order.orderPerson = newOrderPerson
    assert ship_order.orderPerson == newOrderPerson


def test_create_attribute_list(ship_order: etree.ElementTree) -> None:
    """It creates an attribute list that user can get and set properly."""
    assert ship_order.discounts == [1, 2]

    newDiscounts = [3]
    ship_order.discounts = newDiscounts
    assert ship_order.discounts == newDiscounts


def test_fill_in_defaults(ship_order: etree.ElementTree) -> None:
    "It fills defaults properly."
    staticDefaults = {"ShipOrder": {"orderStatus": "wip"}}

    def _get_order_time(element: etree.ElementBase) -> str:
        return element.orderId

    dynamicDefaults = {"ShipOrder": {"orderTime": _get_order_time}}

    fill_in_defaults(ship_order, staticDefaults, dynamicDefaults)
    assert ship_order.orderStatus == staticDefaults["ShipOrder"]["orderStatus"]
    assert ship_order.orderTime == ship_order.orderId


def test_get_element(ship_order: etree.ElementTree) -> None:
    """It gets an element properly."""
    shipTo = ship_order.shipTo
    assert shipTo.name == "Ola Nordmann"


def test_get_element_list(ship_order: etree.ElementTree) -> None:
    """It gets an element list properly."""
    items = ship_order.itemsList
    assert len(items) == 2


def test_get_inner_text_list(ship_order: etree.ElementTree) -> None:
    """It gets an inner text list properly."""
    items = ship_order.itemsList
    assert items[0].notes == ["Item1", "Item1.1"]
