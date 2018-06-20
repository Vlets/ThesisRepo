import pandas as pd
from pandas.io.json import json_normalize
from preprocessing.dataAlgorithms.MFAlgorithm import MFAlgorithm as mfa

class JsonProcessor:

    def json_read(self, filepath, multiline=False):
        file = pd.read_json(filepath, lines=multiline, convert_dates=False)
        return file

    def json_sort(self, file, sort_by):
        if isinstance(sort_by, list):
            sorted_file = file.sort_values(by=sort_by)
            return sorted_file
        raise ValueError("sort_by should be a list indicating column keys: [\"col1\", \"col2\", ...]")

    def normalize_collectors(self, data_frame):
        collector_data = json_normalize(data_frame['collectorData'])
        all_data = pd.concat([collector_data, data_frame], axis=1)
        keep_list = ['visitorId', 'timestamp', 'pageUrl', 'geo.country', 'geo.city', 'geo.continent', 'audience.terms',
                     'categories.terms', 'returningvisitor', 'userAgent', 'globalPersonaIdScores',
                     'personaIdScores']#, 'doctype.terms', 'pageId']
        processed_data = all_data[keep_list]
        print("Step 2/6 - Filtering, done...")
        return processed_data

    def read_and_sort_data(self, file_path):
        sort_by = ["visitorId", "timestamp"]
        data_frame = self.json_read(file_path)
        processed_data = self.normalize_collectors(data_frame)
        sorted_data = self.json_sort(processed_data, sort_by)
        return sorted_data.reset_index(drop=True)

    def do_it_all(self, file_path):
        sorted_data = self.read_and_sort_data(file_path)
        sorted_data.columns = sorted_data.columns.str.replace("[.]", "_")
        transactions = mfa.init_algorithm(sorted_data)
        transaction_dataframe = pd.DataFrame(transactions, columns=['visitorId', 'timestamp', 'transactionPath', 'categories'])
        final_data_frame = pd.merge(transaction_dataframe, sorted_data, on=['visitorId', 'timestamp'])
        return final_data_frame.drop(['timestamp', 'pageUrl', 'categories_terms'], axis=1)

    def json_save(self, sorted_data, savepath, to_json=True):
        if to_json:
            sorted_data.to_json(savepath + ".json", force_ascii=False)
        if not to_json:
            sorted_data.to_csv(savepath + ".csv")