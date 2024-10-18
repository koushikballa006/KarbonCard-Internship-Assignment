from flask import Flask, request, jsonify
from rules import latest_financial_index, iscr_flag, total_revenue_5cr_flag, iscr, borrowing_to_revenue_flag
import json

app = Flask(__name__)

def probe_model_5l_profit(data: dict):
    """
    Evaluate various financial flags for the model.

    :param data: A dictionary containing financial data.
    :return: A dictionary with the evaluated flag values.
    """
    lastest_financial_index_value = latest_financial_index(data)

    total_revenue_5cr_flag_value = total_revenue_5cr_flag(
        data, lastest_financial_index_value
    )

    borrowing_to_revenue_flag_value = borrowing_to_revenue_flag(
        data, lastest_financial_index_value
    )

    iscr_flag_value = iscr_flag(data, lastest_financial_index_value)

    return {
        "flags": {
            "TOTAL_REVENUE_5CR_FLAG": total_revenue_5cr_flag_value,
            "BORROWING_TO_REVENUE_FLAG": borrowing_to_revenue_flag_value,
            "ISCR_FLAG": iscr_flag_value,
        }
    }

@app.route('/api/analyze', method=['POST'])
def analyze_data():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

        file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.json'):
        try:
            data = json.load(file)
            result = probe_model_5l_profit(data["data"])
            return jsonify(result)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON file"}), 400
        except KeyError:
            return jsonify({"error": "Invalid data structure in JSON file"}), 400
    else:
        return jsonify({"error": "Invalid file type. Please upload a JSON file."}), 400        

if __name__ == "__main__":
    # data = json.loads("t.json")
    # print(data)
    with open("data.json", "r") as file:
        content = file.read()
        # convert to json
        data = json.loads(content)
        print(probe_model_5l_profit(data["data"]))
