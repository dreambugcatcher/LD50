from rdkit.Chem import MolFromSmiles, rdFingerprintGenerator as fp
from numpy import zeros
from rdkit import DataStructs
from pandas import DataFrame, MultiIndex
from json import load
from sklearn.preprocessing import StandardScaler


def set_animal(animal):
    # key = 'rat, mouse, rabbit, dog, monkey'
    match animal:
        case None:
            return [0, 0, 0, 0, 0]
        case 'rat':
            return [1, 0, 0, 0, 0]
        case 'mouse':
            return [0, 1, 0, 0, 0]
        case 'rabbit':
            return [0, 0, 1, 0, 0]
        case 'dog':
            return [0, 0, 0, 1, 0]
        case 'monkey':
            return [0, 0, 0, 0, 1]


def set_type(inj):
    # key: oral, ip, iv, sc, dermal, skin
    match inj:
        case None:
            return [0, 0, 0, 0, 0, 0]
        case 'oral':
            return [1, 0, 0, 0, 0, 0]
        case 'ip':
            return [0, 1, 0, 0, 0, 0]
        case 'iv':
            return [0, 0, 1, 0, 0, 0]
        case 'sc':
            return [0, 0, 0, 1, 0, 0]
        case 'dermal':
            return [0, 0, 0, 0, 1, 0]
        case 'skin':
            return [0, 0, 0, 0, 0, 1]


with open('../ld50/data/standardized_data.json', 'r') as file:
    data = load(file)

mfpgen = fp.GetMorganGenerator(radius=2, fpSize=2048)
for_df = []
for id, compinfo in data.items():
    molprint = zeros((1,), dtype=int)
    mol = MolFromSmiles(compinfo['smiles'])
    DataStructs.ConvertToNumpyArray(mfpgen.GetFingerprint(mol), molprint)
    for el in compinfo['ld50']:
        for_df.append(
            (id, molprint,
             *set_animal(el['animal']), *set_type(el['injection']),
             el['value']))

df = DataFrame(for_df)
df.columns = MultiIndex.from_tuples([('id', ''), ('structure', ''),
                                     ('animals', 'rat'),
                                     ('animals', 'mouse'),
                                     ('animals', 'rabbit'),
                                     ('animals', 'dog'),
                                     ('animals', 'monkey'),
                                     ('types', 'oral'),
                                     ('types', 'ip'),
                                     ('types', 'iv'),
                                     ('types', 'sc'),
                                     ('types', 'dermal'),
                                     ('types', 'skin'),
                                     ('value', '')])
# df.to_excel('data/dataframe.xlsx', merge_cells=True)

scaler = StandardScaler()

df['standtr'] = scaler.fit_transform(df[['value']])
print(df)
