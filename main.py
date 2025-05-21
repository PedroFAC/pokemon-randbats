import requests

r = requests.get('https://pkmn.github.io/randbats/data/gen2randombattle.json')
json_data = r.json()
def write_randbats_sets_to_file(json_data):
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

def write_smogon_sets_to_file(json_data, output_path="formatted_sets.txt"):
    def format_evs(evs):
        stat_map = {
            "hp": "HP", "atk": "Atk", "def": "Def",
            "spa": "SpA", "spd": "SpD", "spe": "Spe"
        }
        return " / ".join(f"{v} {stat_map[k]}" for k, v in evs.items() if v != 0)
    def format_ivs(ivs):
        stat_map = {
            "hp": "HP", "atk": "Atk", "def": "Def",
            "spa": "SpA", "spd": "SpD", "spe": "Spe"
        }
        return " / ".join(f"{v} {stat_map[k]}" for k, v in ivs.items() if v != 0)

    def format_moves(moves):
        formatted = []
        for move in moves:
            if isinstance(move, list):
                formatted.append(" / ".join(move))
            else:
                formatted.append(move)
        return "\n".join(f"- {m}" for m in formatted)

    lines = []

    for pokemon, sets in json_data.items():
        for set_name, details in sets.items():
            item = details.get("item", "")
            if isinstance(item, list):
                item = " / ".join(item)

            ability = details.get("ability", "")
            if isinstance(ability, list):
              ability = " / ".join(ability)
            
            tera = details.get("teratypes", "")
            if isinstance(tera, list):
                tera = " / ".join(tera)

            nature = details.get("nature", "")
            if isinstance(nature, list):
              nature = " / ".join(nature)

            evs = details.get("evs", {})
            ivs = details.get("ivs", {})
            if isinstance(evs, list):
                evs = evs[0]
            if isinstance(ivs, list):
                ivs = ivs[0]
            ev_str = format_evs(evs)
            iv_str = format_ivs(ivs)

            if(set_name): 
              lines.append(f"# {pokemon} - {set_name}")
            if item:
              lines.append(f"{pokemon} @ {item}")
            else:
              lines.append(f"{pokemon}")
            if ability:
                lines.append(f"Ability: {ability}")
            if tera:
                lines.append(f"Tera Type: {tera}")
            if ev_str:
                lines.append(f"EVs: {ev_str}")
            if iv_str:
                lines.append(f"IVs: {iv_str}")
            if nature:
                lines.append(f"{nature} Nature")

            lines.append(format_moves(details["moves"]))
            lines.append("")  # Linha em branco entre sets

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

