import csv
from collections import defaultdict
import os
from pprint import pprint
import json

name_data = defaultdict(lambda: defaultdict(int))
for names_file in os.listdir('names'):
    with open(os.path.join('names', names_file), "rU") as f:
        reader = csv.reader(f)

        for line in reader:
            name, sex, count = line
            name_data[sex][name] += int(count)


for entry in name_data:
    name_data[entry] = dict(name_data[entry])

name_data = dict(name_data)

with open('overall_data.json', 'wb') as out:
    json.dump(name_data, out, indent=4)