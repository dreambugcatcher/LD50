from json import load
from numpy import zeros
from rdkit.Chem import MolFromSmiles, rdFingerprintGenerator as fp
from rdkit import DataStructs
from pandas import DataFrame, concat
from sklearn.preprocessing import OneHotEncoder, StandardScaler

with open('data/standardized_data.json', 'r') as file:
    data = load(file)

mfpgen = fp.GetMorganGenerator(radius=2, fpSize=2048)
enc = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
scaler = StandardScaler()

for_df = []
for id, comp in data.items():
    molprint = zeros((1,), dtype=int)
    mol = MolFromSmiles(comp['smiles'])
    DataStructs.ConvertToNumpyArray(mfpgen.GetFingerprint(mol), molprint)
    for el in comp['ld50']:
        value = el['value']
        animal = el['animal']
        inj = el['injection']
        for_df.append([id, molprint, animal, inj, value])

df = DataFrame(for_df, columns=['id', 'structure', 'animal', 'type', 'value'])
onehot_columns = enc.fit_transform(df[['animal']])
df = concat([df, DataFrame(onehot_columns)], axis=1)
encoded_columns_name = enc.get_feature_names_out(['animal'])
dict_column_names = {0: encoded_columns_name[0],
                     1: encoded_columns_name[1],
                     2: encoded_columns_name[2],
                     3: encoded_columns_name[3],
                     4: encoded_columns_name[4]}
df.rename(columns=dict_column_names,
          inplace=True)
print(df.head(15))
# df = DataFrame(for_df_molprints)
