import requests

r = requests.get('https://pkmn.github.io/randbats/data/gen2randombattle.json')
json_data = r.json()
file = open('box.txt', 'w')
for species in json_data:
    species_data = json_data[species]
    roles = species_data['roles']
    level = species_data['level']
    for role in roles:
      role = roles[role]
      if('items' in role ):
        items = role['items']
        species_line = f'{species} @ {items[0]} \n'
      else:
        species_line = f'{species}\n'
      level_line = f'Level: {level} \n'
      file.write(species_line)
      file.write(level_line)
      moves = role['moves']
      for move in moves:
          file.write(f"- {move} \n")
      file.write("\n")
file.close()