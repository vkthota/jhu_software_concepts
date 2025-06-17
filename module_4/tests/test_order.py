# tests/test_order.py

import pytest
from src.order import Order

@pytest.mark.order
def test_order_init():
    """Tests the initialization of an Order object."""
    order = Order()
    assert order.pizzas == []
    assert order.cost == 0.0
    assert not order.paid

@pytest.mark.order
def test_order_input_pizza():
    """Tests adding a pizza to an order and the cost update."""
    order = Order()
    order.input_pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])
    assert len(order.pizzas) == 1
    assert order.cost == 9  # 5 (thin) + 2 (marinara) + 2 (pepperoni)

@pytest.mark.order
def test_order_paid():
    """Tests marking an order as paid."""
    order = Order()
    order.order_paid()
    assert order.paid

@pytest.mark.order
def test_order_str():
    """Tests the string representation of an Order object."""
    order = Order()
    order.input_pizza("thick", ["pesto"], "mozzarella", ["mushrooms"])
    assert "Total Cost: $12" in str(order)