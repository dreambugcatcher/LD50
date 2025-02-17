from rdkit.Chem import MolFromSmiles, rdFingerprintGenerator as fp
from numpy import zeros, hstack, array
from rdkit import DataStructs
from pandas import DataFrame, MultiIndex
from json import load
from sklearn.preprocessing import StandardScaler
from pickle import dump


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
    # key: oral, ip, iv, sc, dermal
    match inj:
        case None:
            return [0, 0, 0, 0, 0]
        case 'oral':
            return [1, 0, 0, 0, 0]
        case 'ip':
            return [0, 1, 0, 0, 0]
        case 'iv':
            return [0, 0, 1, 0, 0]
        case 'sc':
            return [0, 0, 0, 1, 0]
        case 'dermal':
            return [0, 0, 0, 0, 1]


with open('../ld50/data/standardized_data.json', 'r') as file:
    data = load(file)

print(len(data))
for_df_values = []
for_df_prints = []

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

        for_df_values.append(el['value'])
        dop_value = array(set_animal(el['animal'])+set_type(el['injection']))
        for_df_prints.append(hstack((molprint, dop_value)))

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
                                     ('value', '')])


scaler = StandardScaler()
df_Y = DataFrame(for_df_values)
calc_df_X = DataFrame(for_df_prints)
calc_df_Y = scaler.fit_transform(df_Y)
# with open('data/calc_data.pickle', 'wb') as file:
# dump((calc_df_X, calc_df_Y), file)

df.to_excel('data/df.xlsx')
