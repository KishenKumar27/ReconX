from typing import List, Dict

def sort_by_profitability(data: List[Dict], reverse: bool = True) -> List[Dict]:
    """
    Sorts a list of forex data dictionaries based on profitability_percentage in descending order.

    :param
        data: List of forex data dictionaries
        reverse: Boolean flag to sort in descending order

    :return: Sorted list based on profitability_percentage
    """
    return sorted(data, key=lambda x: float(x["profitability_percentage"]), reverse=reverse)