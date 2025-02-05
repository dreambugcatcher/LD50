import json as js
from pickle import dump


def search_value(item, key_word):
    if (isinstance(item, str) and key_word in item
       and '/kg' in item[item.index(key_word):item.index(key_word)+30]):
        yield item
    elif isinstance(item, list):
        for el in item:
            yield from search_value(el, key_word)
    elif isinstance(item, dict):
        for keys in item:
            yield from search_value(item[keys], key_word)


dict_of_values = {}
with open('data/cids_and_smiles2.json', 'r') as file:
    cids_and_smiles = js.load(file)

for el in cids_and_smiles:
    id = el[0]
    with open(f'data/raw2/{id}.json', 'r') as file:
        data = js.load(file)
    print(id)
    SMILES = el[1]
    value = list(search_value(data, 'LD50'))
    if len(value):
        dict_of_values[id] = {'smiles': SMILES, 'LD50': value}

print(f'{len(dict_of_values)=}')
with open('data/dict_of_values2.pickle', 'wb') as data:
    dump(dict_of_values, data)
