from rdkit.Chem import MolFromSmiles
from rdkit.Chem import Descriptors as Ds
from json import load, dump


def convert(molecule, value, unit):
    if ('-' in value) and ('e' not in value):
        value = sum(map(float, value.split('-')))/2
    mol_weight = Ds.MolWt(MolFromSmiles(molecule))
    match unit:
        case 'mg/kg':
            pass
        case 'g/kg':
            value = float(value) * 1000
        case 'ug/kg':
            value = float(value) / 1000
        case 'mmol/kg':
            value = round(float(value) * mol_weight, 3)
        case 'ml/kg':
            # unit = unit * (mol_weight/mol_density)
            pass
        case 'ul/kg':
            # unit = unit * (mol_weight/mol_density)
            pass

    unit = 'mg/kg'
    return round(float(value), 5), unit


with open('data/data_without_dubl.json', 'r') as file:
    data = load(file)

for id in data.copy():
    molecule = data[id]['smiles']
    for el in data[id]['ld50'].copy():
        unit = el['measure']
        if ('ml/kg' in unit) or ('ul/kg' in unit):
            del data[id]['ld50'][data[id]['ld50'].index(el)]
            print(id)
            continue
        else:
            value = el['value']
        el['value'], el['measure'] = convert(molecule, value, unit)
        for keys in el:
            if el[keys] == "search_error":
                el[keys] = None
    if not len(data[id]['ld50']):
        del data[id]

with open('data/standardized_data.json', 'w') as file:
    dump(data, file, indent=4)
