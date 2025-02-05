from json import load
import chython as ch


def max_size(input_list):
    sizes = tuple(len(el) for el in input_list)
    return input_list[sizes.index(max(sizes))]


with open('data/data_without_dubl.json', 'r') as database:
    data = load(database)

list_of_smiles = [(id, data[id]['smiles']) for id in data]

for id, molecule in zip((el[0] for el in list_of_smiles),
                        (el[1] for el in list_of_smiles)):
    molecule_in = molecule
    if '.' in molecule:
        molecule = max_size(molecule.split('.'))
        data[id]['smiles'] = molecule

    try:
        molecule = ch.smiles(molecule, ignore=True)
        molecule.thiele()
        molecule.neutralize()
        molecule.canonicalize()
        if molecule.check_valence():
            print(f'Ошибки в атомах: {molecule.check_valence()}')
            print(molecule)
        data[id]['smiles'] = str(molecule)
    except ch.exceptions.InvalidAromaticRing:
        print(f'Ошибка кекуле! {id}')
        print(molecule)
