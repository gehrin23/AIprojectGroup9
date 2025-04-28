Here is the revised source code with added inline comments and docstrings:
```python
def calculate_total(items):
    """
    Calculates the total cost of a list of items.

    :param items: A list of items, where each item has a price attribute.
    :return: The total cost of all items in the list.
    """
    total = 0
    for item in items:
        total += item.price
    return total

def calculate_discount(total):
    """
    Calculates the discount on a given total cost.

    :param total: The total cost of an order.
    :return: The discount amount applied to the order.
    """
    if total < 100:
        return 0
    elif total >= 100 and total < 500:
        return total * 0.1
    else:
        return total * 0.2

def apply_discount(total, discount):
    """
    Applies a discount to a given total cost.

    :param total: The total cost of an order.
    :param discount: The discount amount applied to the order.
    :return: The updated total cost after applying the discount.
    """
    return total - discount
```
Overall file purpose:
The purpose of this file is to provide a set of functions for calculating totals and discounts for an online shopping platform. These functions can be used to calculate the total cost of an order, apply a discount, and update the total cost after applying a discount.

Key functions/methods:
The key functions in this file are `calculate_total`, `calculate_discount`, and `apply_discount`. These functions each have specific responsibilities and inputs, outputs, side effects, design patterns, dependencies, cohesion, and coupling.

* calculate_total: This function takes a list of items as input and returns the total cost of all items in the list. It has no side effects, uses the add operator to calculate the total cost, and depends on the price attribute of each item in the list. The cohesion is high because the function only does one thing, which is to calculate the total cost of a list of items.
* calculate_discount: This function takes a total cost as input and returns the discount amount applied to that cost. It has no side effects, uses if-else statements to determine the discount amount based on the total cost, and depends on the total cost input parameter. The cohesion is high because the function only does one thing, which is to calculate the discount amount based on the total cost.
* apply_discount: This function takes a total cost and a discount amount as input and returns the updated total cost after applying the discount. It has no side effects, uses the subtraction operator to update the total cost, and depends on both the total cost and discount amount inputs. The cohesion is high because the function only does one thing, which is to apply a discount to an order.

Inputs/outputs:
The inputs for each of these functions are as follows:

* calculate_total: A list of items where each item has a price attribute. The output is the total cost of all items in the list.
* calculate_discount: The total cost of an order as input and returns the discount amount applied to that cost.
* apply_discount: A total cost and a discount amount as inputs and returns the updated total cost after applying the discount.

Design patterns, dependencies:
The functions in this file use design patterns such as the add operator and subtraction operator to perform their calculations. The functions also depend on the price attribute of each item in the list for calculating the total cost.

Point out cohesion and coupling:
* calculate_total has high cohesion because it only does one thing, which is to calculate the total cost of a list of items.
* calculate_discount has high cohesion because it only does one thing, which is to calculate the discount amount based on the total cost.
* apply_discount has high cohesion because it only does one thing, which is to apply a discount to an order.
* The coupling of these functions is low because they do not share any global state or rely on each other for their functionality.