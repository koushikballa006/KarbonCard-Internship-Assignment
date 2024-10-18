from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, borrowing_to_revenue_flag
import json

def probe_model_5l_profit(data: dict):
    """
    Evaluate various financial flags for the model.
    :param data: A dictionary containing financial data.
    :return: A dictionary with the evaluated flag values.
    """
    latest_financial_index_value = latest_financial_index(data)
    total_revenue_5cr_flag_value = total_revenue_5cr_flag(
        data, latest_financial_index_value
    )
    borrowing_to_revenue_flag_value = borrowing_to_revenue_flag(
        data, latest_financial_index_value
    )
    iscr_flag_value = iscr_flag(data, latest_financial_index_value)
    return {
        "flags": {
            "TOTAL_REVENUE_5CR_FLAG": total_revenue_5cr_flag_value,
            "BORROWING_TO_REVENUE_FLAG": borrowing_to_revenue_flag_value,
            "ISCR_FLAG": iscr_flag_value,
        }
    }

def analyze_json_data(json_data: str):
    """
    Analyze JSON data containing financial information.
    :param json_data: JSON string containing financial data.
    :return: Analysis result.
    """
    try:
        data = json.loads(json_data)
        return probe_model_5l_profit(data["data"])
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON data")
    except KeyError:
        raise ValueError("Invalid data structure in JSON")

if __name__ == "__main__":
    # This code runs when you execute the script directly
    with open("data.json", "r") as file:
        content = file.read()
    result = analyze_json_data(content)
    print(result)