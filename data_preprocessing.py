from pickle import load

with open('data/dict_of_values1.pickle', 'rb') as database:
    data = load(database)

smiles = [data[id]['smiles'] for id in data]
cids_and_smiles = {id: data[id]['smiles'] for id in data}

for id, smile in cids_and_smiles.items():
    if '.' in smile:
        del data[id]
    elif '[' in smile:
        del data[id]

print(len(data))
print(data)
