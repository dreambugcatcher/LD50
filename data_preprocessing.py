from json import load, dump
import chython as ch


with open('data/data_without_dubl.json', 'r') as database:
    data = load(database)

list_of_smiles = [(id, data[id]['smiles']) for id in data]

for el in list_of_smiles:
    id, molecule = el
    if '.' in molecule:
        molecule = max(molecule.split('.'), key=len)
        data[id]['smiles'] = molecule

    try:
        molecule = ch.smiles(molecule, ignore=True)
        molecule.clean_isotopes()
        molecule.canonicalize()
        if molecule.check_valence():
            # print(f'Ошибки в атомах: {molecule.check_valence()}')
            # print(molecule)
            del data[id]
            continue
        data[id]['smiles'] = str(molecule)
    except ch.exceptions.InvalidAromaticRing:
        print(f'Ошибка кекуле! {id}')
        print(molecule)

with open('data/data_without_dubl.json', 'w') as file:
    dump(data, file, indent=4)
