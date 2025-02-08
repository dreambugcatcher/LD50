import pandas as pd
# import json as js

data = pd.read_csv(
 'data/PubChem_compound_cache_qe4PNUGJJDUTG6wCLnrlK3S7tts4HVrIIO1BhDv8U4U75W8.csv')

cids = data[' cid'].tolist()
smiles = data['smiles'].tolist()

cids_and_smiles = []

for cid, smile in zip(cids, smiles):
    cids_and_smiles.append((cid, smile))

# with open('data/cids_and_smiles2.json', 'w') as file:
    # js.dump(cids_and_smiles, file)
