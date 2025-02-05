from pickle import load
from json import dump


with open('data/dict_of_values1.pickle', 'rb') as file:
    data_in = load(file)

with open('data/dict_of_values1.json', 'w') as file:
    dump(data_in, file)
