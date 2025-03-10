#!/usr/bin/env python3
"""
Basic usage examples for the PokéAPI wrapper
"""

import sys

sys.path.append("../..")  # this is including the parent directory in the path

from pokeapi_wrapper.api import PokeAPI


def main():
    """
    Main function to demonstrate the usage of the PokéAPI wrapper
    """
    # Initialize the API client
    api = PokeAPI()

    print("Fetching Pikachu...")
    pikachu = api.get_pokemon("pikachu")
    print(f"Name: {pikachu.name}")
    print(f"ID: {pikachu.id}")
    print(f"Height: {pikachu.height/10} m")  # Height is in decimeters
    print(f"Weight: {pikachu.weight/10} kg")  # Weight is in hectograms

    print("\nTypes:")
    for type_info in pikachu.types:
        print(f"- {type_info.type['name']}")

    print("\nAbilities:")
    for ability_info in pikachu.abilities:
        hidden_text = " (hidden)" if ability_info.is_hidden else ""
        print(f"- {ability_info.ability['name']}{hidden_text}")

    # Display colored ASCII art of Pikachu
    print("\nPikachu Colored ASCII Art:")
    pikachu.get_ascii_sprite(width=60)

    print("\nFetching Charizard...")
    charizard = api.get_pokemon("charizard")
    print(f"Name: {charizard.name}")

    # Display ASCII art of Charizard (front)
    print("\nCharizard ASCII Art (Front):")
    charizard.get_ascii_sprite(width=70)

    # Try a few more Pokémon
    print("\nFetching Gengar...")
    gengar = api.get_pokemon("gengar")
    print(f"Name: {gengar.name}")

    print("\nGengar ASCII Art:")
    gengar.get_ascii_sprite(width=60)

    print("\nFetching a list of Pokemon...")
    pokemon_list = api.get_pokemon_list(limit=5)
    print(f"Total count: {pokemon_list.count}")

    print("\nResults:")
    for pokemon in pokemon_list.results:
        print(f"- {pokemon['name']} (ID: {pokemon['id']})")


if __name__ == "__main__":
    main()
