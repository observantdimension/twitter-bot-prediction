import shared
import bqml
import json


def run_app():
    predicted_records = {x['name']: x['predicted_label'] for x in bqml.predict_data()}

    with open('generated_data/user_predictions.json', 'w', encoding='utf-8') as file:
        json.dump(predicted_records, file, sort_keys=True, indent=4, ensure_ascii=False)
    print("dumped predictions")


run_app()
