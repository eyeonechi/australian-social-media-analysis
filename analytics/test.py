import json
file_name = "test.json"
input_file = open(file_name)
data = json.load(input_file)
input_file.close()

print(data['polarity'])