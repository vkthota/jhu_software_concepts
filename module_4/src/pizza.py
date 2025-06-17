# src/pizza.py

class Pizza:
    """
    A class to represent a single pizza with its toppings and calculate its cost.

    Attributes:
        crust (str): The type of crust for the pizza.
        sauces (list): A list of sauces on the pizza.
        cheese (str): The type of cheese on the pizza.
        toppings (list): A list of toppings on the pizza.
        cost (float): The total cost of the pizza.
    """

    COST_VARIABLES = {
        "crust": {"thin": 5, "thick": 6, "gluten-free": 8},
        "sauce": {"marinara": 2, "pesto": 3, "liv sauce": 5},
        "topping": {"pineapple": 1, "pepperoni": 2, "mushrooms": 3},
        "cheese": {"mozzarella": 0}  # Assuming mozzarella is the default and included
    }

    def __init__(self, crust, sauces, cheese, toppings):
        """
        Initializes a Pizza object.

        Args:
            crust (str): The type of crust.
            sauces (list): A list of sauces.
            cheese (str): The type of cheese.
            toppings (list): A list of toppings.
        """
        self.crust = crust
        self.sauces = sauces
        self.cheese = cheese
        self.toppings = toppings
        self.cost = self.calculate_cost()

    def calculate_cost(self):
        """Calculates the total cost of the pizza based on its ingredients."""
        total_cost = 0
        total_cost += self.COST_VARIABLES["crust"].get(self.crust.lower(), 0)
        for sauce in self.sauces:
            total_cost += self.COST_VARIABLES["sauce"].get(sauce.lower(), 0)
        for topping in self.toppings:
            total_cost += self.COST_VARIABLES["topping"].get(topping.lower(), 0)
        # Assuming cheese cost is included or free as per the limited description
        return total_cost

    def __str__(self):
        """Returns a string representation of the pizza."""
        return (f"Crust: {self.crust}, Sauces: {self.sauces}, Cheese: {self.cheese}, "
                f"Toppings: {self.toppings}, Cost: ${self.cost}")