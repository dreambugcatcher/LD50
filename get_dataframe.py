from rdkit.Chem import MolFromSmiles, AllChem
from numpy import zeros
from rdkit import DataStructs
from pandas import DataFrame
from json import load


def calc_morgan(mols):
    """ генерация молекулярных отпечатков по методу Моргана с радиусом 2 и
    длиной 2048
    """
    for_df = []
    for m in mols:
        arr = zeros((1,), dtype=int)
        DataStructs.ConvertToNumpyArray(
            AllChem.GetMorganFingerprintAsBitVect(m, 2, 2048), arr)
        for_df.append(arr)
    return DataFrame(for_df)


with open('data/standardized_data.json', 'r') as file:
    data = load(file)

molecules = []
for comp in data.values():
    molecules.append(MolFromSmiles(comp['smiles']))

calc_morgan(molecules)
