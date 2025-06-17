# tests/test_pizza.py

import pytest
from src.pizza import Pizza

@pytest.mark.pizza
def test_pizza_init():
    """Tests the initialization of a Pizza object."""
    pizza = Pizza("thin", ["marinara"], "mozzarella", ["pepperoni"])
    assert pizza.crust == "thin"
    assert pizza.sauces == ["marinara"]
    assert pizza.cheese == "mozzarella"
    assert pizza.toppings == ["pepperoni"]
    assert pizza.cost > 0

@pytest.mark.pizza
def test_pizza_cost():
    """Tests the cost calculation of a pizza."""
    pizza = Pizza("thin", ["marinara"], "mozzarella", ["pineapple", "pepperoni"])
    # 5 (thin) + 2 (marinara) + 1 (pineapple) + 2 (pepperoni) = 10
    assert pizza.calculate_cost() == 10

@pytest.mark.pizza
def test_pizza_str():
    """Tests the string representation of a Pizza object."""
    pizza = Pizza("thick", ["pesto"], "mozzarella", ["mushrooms"])
    assert "Crust: thick" in str(pizza)
    assert "Cost: $12" in str(pizza)