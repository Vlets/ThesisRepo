from preprocessing.helpers.JsonProcessor import JsonProcessor
import preprocessing.dataFiles.mockData as dataFiles
import time

jsonTools = JsonProcessor()

filePath = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/preprocessing/Joana/test_mb.json"


# THE ONE FUNCTION TO RULE THEM ALL IS do_it_all(filePath)

start = time.time()
final_dataframe = jsonTools.do_it_all(filePath)
end = time.time()

print(end-start, "- Seconds")

# TODO: RUN LOOOOOOTS OF TESTS TO CONFIRM RESULTS

# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
# jsonTools.json_save(sortedData, "./dataFiles/testProduced", toJson=False)
