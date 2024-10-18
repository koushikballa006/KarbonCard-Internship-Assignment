import datetime

class FLAGS:
    GREEN = 1
    AMBER = 2
    RED = 0
    MEDIUM_RISK = 3  # display purpose only
    WHITE = 4  # data is missing for this field

def latest_financial_index(data: dict):
    """
    Determine the index of the latest standalone financial entry in the data.

    This function iterates over the "financials" list in the given data dictionary.
    It returns the index of the first financial entry where the "nature" key is equal to "STANDALONE".
    If no standalone financial entry is found, it returns 0.

    Parameters:
    - data (dict): A dictionary containing a list of financial entries under the "financials" key.

    Returns:
    - int: The index of the latest standalone financial entry or 0 if not found.
    """
    for index, financial in enumerate(data.get("financials", [])):
        if financial.get("nature") == "STANDALONE":
            return index
    return 0

def total_revenue(data: dict, financial_index: int) -> float:
    """
    Calculate the total revenue from the financial data at the given index.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The net revenue value from the financial data.
    """
    try:
        return data["financials"][financial_index]["pnl"]["lineItems"]["net_revenue"]
    except (KeyError, IndexError):
        return 0.0

def total_borrowing(data: dict, financial_index: int) -> float:
    """
    Calculate the total borrowings from the financial data at the given index.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for calculation.

    Returns:
    - float: The sum of long-term and short-term borrowings.
    """
    try:
        bs = data["financials"][financial_index]["bs"]["liabilities"]
        return bs.get("long_term_borrowings", 0) + bs.get("short_term_borrowings", 0)
    except (KeyError, IndexError):
        return 0.0

def iscr(data: dict, financial_index: int) -> float:
    """
    Calculate the Interest Service Coverage Ratio (ISCR) for the financial data at the given index.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - float: The ISCR value.
    """
    try:
        pnl = data["financials"][financial_index]["pnl"]["lineItems"]
        profit_before_interest_and_tax = pnl.get("profit_before_interest_and_tax", 0)
        depreciation = pnl.get("depreciation", 0)
        interest = pnl.get("interest", 0)
        
        numerator = profit_before_interest_and_tax + depreciation + 1
        denominator = interest + 1
        
        return numerator / denominator
    except (KeyError, IndexError):
        return 0.0

def iscr_flag(data: dict, financial_index: int) -> int:
    """
    Determine the flag color based on the Interest Service Coverage Ratio (ISCR) value.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ISCR calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the ISCR value.
    """
    iscr_value = iscr(data, financial_index)
    return FLAGS.GREEN if iscr_value >= 2 else FLAGS.RED

def total_revenue_5cr_flag(data: dict, financial_index: int) -> int:
    """
    Determine the flag color based on whether the total revenue exceeds 50 million.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the revenue calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.RED: The flag color based on the total revenue.
    """
    revenue = total_revenue(data, financial_index)
    return FLAGS.GREEN if revenue >= 50000000 else FLAGS.RED

def borrowing_to_revenue_flag(data: dict, financial_index: int) -> int:
    """
    Determine the flag color based on the ratio of total borrowings to total revenue.

    Parameters:
    - data (dict): A dictionary containing financial data.
    - financial_index (int): The index of the financial entry to be used for the ratio calculation.

    Returns:
    - FLAGS.GREEN or FLAGS.AMBER: The flag color based on the borrowing to revenue ratio.
    """
    revenue = total_revenue(data, financial_index)
    borrowing = total_borrowing(data, financial_index)
    
    if revenue == 0:
        return FLAGS.AMBER
    
    ratio = borrowing / revenue
    return FLAGS.GREEN if ratio <= 0.25 else FLAGS.AMBER