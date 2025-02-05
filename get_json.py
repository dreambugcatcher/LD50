import requests as rq
import json as js
# from time import sleep

with open('data/cids_and_smiles2.json', 'r') as cids:
    database = js.load(cids)

for el in database:
    if el[0] > 26575:
        id = el[0]
        print(id)
        flag = False
        while not flag:
            try:
                data = rq.get(
                 f'https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{id}/JSON',
                 timeout=5)
                flag = True
            except rq.exceptions.ReadTimeout:
                pass

        with open(
            f'data/raw2/{id}.json', 'w', encoding='utf-8'
                ) as file:
            js.dump(data.json(), file, ensure_ascii=False, indent=4)
