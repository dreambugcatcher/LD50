from pickle import load

with open('data/dict_of_values1.pickle', 'rb') as file:
    data = load(file)

rat_counter = 0
mouse_counter = 0
dog_counter = 0
hamster_counter = 0
rabbit_counter = 0
monkey_counter = 0

for values in data.values():
    for el in values['LD50']:
        rat_counter += 1 if 'rat' in el.lower() else 0
        mouse_counter += 1 if 'mouse' in el.lower() else 0
        dog_counter += 1 if 'dog' in el.lower() else 0
        hamster_counter += 1 if 'hamster' in el.lower() else 0
        rabbit_counter += 1 if 'rabbit' in el.lower() else 0
        monkey_counter += 1 if 'monkey' in el.lower() else 0

print(f'Число крыс: {rat_counter}',
      f'Число мышей: {mouse_counter}',
      f'Число собак: {dog_counter}',
      f'Число хомяков: {hamster_counter}',
      f'Число кроликов: {rabbit_counter}',
      f'Число обезьян: {monkey_counter}', sep='\n')
