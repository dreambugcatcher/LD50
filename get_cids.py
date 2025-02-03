import pandas as pd
import json as js

data = pd.read_csv(
 'PubChem_compound_cache_P3iZBvJNl_Gg25XCF7rc63eakPpV556a5L-F1v-ul9f_t6s.csv')

cids = data[' cid'].tolist()
smiles = data['smiles'].tolist()

cids_and_smiles = []

for cid, smile in zip(cids, smiles):
    cids_and_smiles.append((cid, smile))

with open('cids_and_smiles.json', 'w') as file:
    js.dump(cids_and_smiles, file)
