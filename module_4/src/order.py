# src/order.py

from pizza import Pizza

class Order:
    """
    A class to represent a customer's pizza order.

    Attributes:
        pizzas (list): A list of Pizza objects in the order.
        cost (float): The total cost of the order.
        paid (bool): A boolean indicating if the order has been paid for.
    """

    def __init__(self):
        """Initializes an Order object."""
        self.pizzas = []
        self.cost = 0.0
        self.paid = False

    def input_pizza(self, crust, sauces, cheese, toppings):
        """Creates a new pizza and adds it to the order."""
        new_pizza = Pizza(crust, sauces, cheese, toppings)
        self.pizzas.append(new_pizza)
        self.update_cost()

    def update_cost(self):
        """Updates the total cost of the order by summing the costs of all pizzas."""
        self.cost = sum(pizza.cost for pizza in self.pizzas)

    def order_paid(self):
        """Marks the order as paid."""
        self.paid = True

    def __str__(self):
        """Returns a string representation of the entire order."""
        if not self.pizzas:
            return "Customer Order: No pizzas in the order. Total Cost: $0.0"

        order_details = "Customer Order:\n"
        for pizza in self.pizzas:
            order_details += f"  - {pizza}\n"
        order_details += f"Total Cost: ${self.cost}"
        return order_details