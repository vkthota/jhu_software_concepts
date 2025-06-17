# tests/test_integration.py

import pytest
from src.order import Order

@pytest.mark.order
@pytest.mark.pizza
def test_multiple_pizzas_in_order():
    """Tests that an order can handle multiple pizzas and calculates the total cost correctly."""
    order = Order()
    # Pizza 1: thin, marinara, pineapple = 5 + 2 + 1 = 8
    order.input_pizza("thin", ["marinara"], "mozzarella", ["pineapple"])

    # Pizza 2: thick, pesto, pepperoni, mushrooms = 6 + 3 + 2 + 3 = 14
    order.input_pizza("thick", ["pesto"], "mozzarella", ["pepperoni", "mushrooms"])

    assert len(order.pizzas) == 2
    assert order.cost == 22  # 8 + 14
    assert "Cost: $8" in str(order.pizzas[0])
    assert "Cost: $14" in str(order.pizzas[1])
    assert "Total Cost: $22" in str(order)