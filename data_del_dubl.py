from json import load, dump

with open('data/data_with_dubl.json', 'r') as file:
    data = load(file)

for comp in data.values():  # Удаление "полных" дублей
    list_of_values = comp['ld50']
    new_values = []
    if len(list_of_values) == 1:
        continue
    else:
        generate_list = tuple(tuple(el.values()) for el in list_of_values)
        for indx, value in enumerate(generate_list):
            if generate_list.count(value) == 1:
                new_values.append(list_of_values[indx])
            elif (generate_list.count(value) > 1
                  and (list_of_values[indx] not in new_values)):
                new_values.append(list_of_values[indx])
    comp['ld50'] = new_values


with open('data/data_without_dubl.json', 'w') as file:
    dump(data, file, indent=4)
