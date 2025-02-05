from pickle import load
# from json import dump
from copy import deepcopy


def search_animal(text):
    text = text.lower()
    text = text.replace('mice', 'mouse')
    animals = {'rat', 'dog', 'mouse', 'rabbit', 'monkey'}
    for animal in animals:
        if animal in text:
            return animal
    else:
        return 'search_error'


def search_type(text):
    text = text.lower()
    text = text.replace('peroral', 'oral')
    text = text.replace('i.v.', 'iv')
    injections = {'oral', 'skin', 'ip', 'iv', 'dermal', 'sc'}
    for el in injections:
        if el in text:
            return el
    else:
        return 'search_error'


def search_measure(text):
    for el in text.split():
        if '/kg' in el:
            return el
    else:
        return 'search_error'


def search_value(text):
    for el in text.split():
        el = el.replace(',', '.')
        if el.replace('.', '').replace('-', '').isdigit():
            return el
        elif '>' in el or '<' in el:
            if el.lstrip('<>').replace('.', '').replace('-', '').isdigit():
                return el
    else:
        return 'search_error'


with open('data/dict_of_values1.pickle', 'rb') as file:
    data = load(file)

data_in = deepcopy(data)

for id, values in data.items():
    new_ld50 = []
    for el in values['LD50']:
        if '\n' in el:
            new_ld50.extend(el.split('\n'))
        elif len(el) > 40:
            while 'LD50' in el:
                if ('/kg' in el) and (el.find('LD50') < el.find('/kg')+3):
                    add_el = el[el.find('LD50'): el.find('/kg')+3]
                    new_ld50.append(add_el)
                    el = el.replace(add_el, '')
                else:
                    el = str()
        else:
            new_ld50.append(el)
    values['LD50'] = new_ld50

for id in data.copy():
    if not len(data[id]['LD50']):
        del data[id]

pure_data = {}
for id in data:
    smiles = data[id]['smiles']
    ld50_value = data[id]['LD50']
    new_ld50_value = []
    for el in ld50_value:
        el = el.replace('LD50', '')
        animal = search_animal(el)
        injection = search_type(el)
        measure = search_measure(el)
        value = search_value(el)
        if (animal == 'search_error'
           and 'search_error' in value):
            continue
        new_ld50_value.append(
            {'animal': animal,
             'injection': injection,
             'value': value+' '+measure}
        )
    pure_data[id] = {'smiles': smiles,
                     'ld50': new_ld50_value}

# with open('data/pure_data.json', 'w') as file:
    # dump(pure_data, file, indent=4)
