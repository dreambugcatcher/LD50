import requests as rq
import json as js
# from time import sleep

with open('cid.json', 'r') as cids:
    CIDs = js.load(cids)

counter = 0
for id in CIDs[CIDs.index(3054304):]:
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
        f'/home/titovetsla/data/{id}.json', 'w', encoding='utf-8'
              ) as file:
        js.dump(data.json(), file, ensure_ascii=False, indent=4)
