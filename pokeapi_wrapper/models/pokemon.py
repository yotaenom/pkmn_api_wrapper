"""
Pokemon models for the PokéAPI wrapper
"""

from .base import NamedAPIResource, VersionGameIndex
from ascii_magic import AsciiArt


class PokemonAbility:
    """Pokemon ability model"""

    def __init__(self, is_hidden=False, slot=None, ability=None, **kwargs):
        self.is_hidden = is_hidden
        self.slot = slot
        self.ability = ability


class PokemonType:
    """Pokemon type model"""

    def __init__(self, slot=None, type=None, **kwargs):
        self.slot = slot
        self.type = type


class PokemonHeldItemVersion:
    """Pokemon held item version model"""

    def __init__(self, version=None, rarity=None, **kwargs):
        self.version = version
        self.rarity = rarity


class PokemonHeldItem:
    """Pokemon held item model"""

    def __init__(self, item=None, version_details=None, **kwargs):
        self.item = item
        self.version_details = version_details or []


class PokemonMoveVersion:
    """Pokemon move version model"""

    def __init__(
        self,
        move_learn_method=None,
        version_group=None,
        level_learned_at=None,
        **kwargs,
    ):
        self.move_learn_method = move_learn_method
        self.version_group = version_group
        self.level_learned_at = level_learned_at


class PokemonMove:
    """Pokemon move model"""

    def __init__(self, move=None, version_group_details=None, **kwargs):
        self.move = move
        self.version_group_details = version_group_details or []


class PokemonStat:
    """Pokemon stat model"""

    def __init__(self, stat=None, effort=None, base_stat=None, **kwargs):
        self.stat = stat
        self.effort = effort
        self.base_stat = base_stat


class PokemonSprites:
    """Pokemon sprites model"""

    def __init__(
        self,
        front_default=None,
        front_shiny=None,
        front_female=None,
        front_shiny_female=None,
        back_default=None,
        back_shiny=None,
        back_female=None,
        back_shiny_female=None,
        other=None,
        versions=None,
        **kwargs,
    ):
        self.front_default = front_default
        self.front_shiny = front_shiny
        self.front_female = front_female
        self.front_shiny_female = front_shiny_female
        self.back_default = back_default
        self.back_shiny = back_shiny
        self.back_female = back_female
        self.back_shiny_female = back_shiny_female
        self.other = other or {}
        self.versions = versions or {}


class PokemonTypePast:
    """Pokemon type past model"""

    def __init__(self, generation=None, types=None, **kwargs):
        self.generation = generation
        self.types = types or []


class Pokemon:
    """Pokemon model"""

    def __init__(
        self,
        id=None,
        name=None,
        base_experience=None,
        height=None,
        is_default=False,
        order=None,
        weight=None,
        abilities=None,
        forms=None,
        game_indices=None,
        held_items=None,
        location_area_encounters=None,
        moves=None,
        past_types=None,
        sprites=None,
        species=None,
        stats=None,
        types=None,
        **kwargs,
    ):
        # Process nested objects before assigning to attributes
        if abilities is not None:
            abilities = (
                [PokemonAbility(**ability) for ability in abilities]
                if isinstance(abilities[0], dict)
                else abilities
            )

        if types is not None:
            types = (
                [PokemonType(**type_data) for type_data in types]
                if isinstance(types[0], dict)
                else types
            )

        if stats is not None:
            stats = (
                [PokemonStat(**stat) for stat in stats]
                if isinstance(stats[0], dict)
                else stats
            )

        if moves is not None:
            processed_moves = []
            for move_data in moves:
                if isinstance(move_data, dict):
                    move_copy = dict(move_data)
                    if (
                        "version_group_details" in move_copy
                        and move_copy["version_group_details"]
                    ):
                        move_copy["version_group_details"] = [
                            PokemonMoveVersion(**detail)
                            for detail in move_copy["version_group_details"]
                        ]
                    processed_moves.append(PokemonMove(**move_copy))
                else:
                    processed_moves.append(move_data)
            moves = processed_moves

        if held_items is not None:
            processed_held_items = []
            for item_data in held_items:
                if isinstance(item_data, dict):
                    item_copy = dict(item_data)
                    if "version_details" in item_copy and item_copy["version_details"]:
                        item_copy["version_details"] = [
                            PokemonHeldItemVersion(**detail)
                            for detail in item_copy["version_details"]
                        ]
                    processed_held_items.append(PokemonHeldItem(**item_copy))
                else:
                    processed_held_items.append(item_data)
            held_items = processed_held_items

        if sprites is not None and isinstance(sprites, dict):
            sprites = PokemonSprites(**sprites)

        if species is not None and isinstance(species, dict):
            species = NamedAPIResource(**species)

        if forms is not None:
            forms = [
                NamedAPIResource(**form) if isinstance(form, dict) else form
                for form in forms
            ]

        if game_indices is not None:
            game_indices = [
                VersionGameIndex(**index) if isinstance(index, dict) else index
                for index in game_indices
            ]

        if past_types is not None:
            processed_past_types = []
            for past_type_data in past_types:
                if isinstance(past_type_data, dict):
                    past_type_copy = dict(past_type_data)
                    if "types" in past_type_copy:
                        past_type_copy["types"] = [
                            PokemonType(**t) for t in past_type_copy["types"]
                        ]
                    if "generation" in past_type_copy and isinstance(
                        past_type_copy["generation"], dict
                    ):
                        past_type_copy["generation"] = NamedAPIResource(
                            **past_type_copy["generation"]
                        )
                    processed_past_types.append(PokemonTypePast(**past_type_copy))
                else:
                    processed_past_types.append(past_type_data)
            past_types = processed_past_types

        # Assign all attributes
        self.id = id
        self.name = name
        self.base_experience = base_experience
        self.height = height
        self.is_default = is_default
        self.order = order
        self.weight = weight
        self.abilities = abilities or []
        self.forms = forms or []
        self.game_indices = game_indices or []
        self.held_items = held_items or []
        self.location_area_encounters = location_area_encounters
        self.moves = moves or []
        self.past_types = past_types or []
        self.sprites = sprites
        self.species = species
        self.stats = stats or []
        self.types = types or []

    def get_ascii_sprite(self, width=40, shiny=False, back=False, colored=True):
        """
        Get an ASCII representation of the Pokemon's sprite using ascii_magic

        Args:
            width: Width of the ASCII art in columns (default: 40)
            height: Height of the ASCII art in rows (default: 20)
            shiny: Whether to use the shiny sprite (default: False)
            back: Whether to use the back sprite (default: False)
            colored: Whether to use colored ASCII art (default: True)

        Returns:
            ASCII art string or None if the sprite couldn't be loaded
        """

        # Determine which sprite to use
        sprite_url = None
        if self.sprites:
            if back:
                sprite_url = (
                    self.sprites.back_shiny if shiny else self.sprites.back_default
                )
            else:
                sprite_url = (
                    self.sprites.front_shiny if shiny else self.sprites.front_default
                )

        # Convert the sprite to ASCII
        if sprite_url:
            return AsciiArt.from_url(sprite_url).to_terminal(columns=width)
        else:
            return None

    def show_pokemon(self, colored=True):
        """
        Display the Pokémon's characteristics and ASCII sprite in the terminal

        Args:
            colored: Whether to use colored ASCII art (default: True)
        """
        # Get the ASCII sprite
        ascii_sprite = self.get_ascii_sprite(width=60, colored=colored)

        # Create a header with the Pokémon's name and ID
        name = self.name.upper()
        pokemon_id = f"#{self.id:03d}"
        header = f"=== {name} {pokemon_id} ==="
        separator = "=" * len(header)

        # Format the Pokémon's characteristics
        height_m = self.height / 10  # Convert from decimeters to meters
        weight_kg = self.weight / 10  # Convert from hectograms to kilograms

        # Get types
        types = [t.type["name"].capitalize() for t in self.types]
        types_str = "/".join(types)

        # Get abilities
        abilities = []
        for a in self.abilities:
            ability_name = a.ability["name"].replace("-", " ").capitalize()
            if a.is_hidden:
                ability_name += " (Hidden)"
            abilities.append(ability_name)
        abilities_str = ", ".join(abilities)

        # Get base stats if available
        stats_str = ""
        if self.stats:
            stats = {}
            for s in self.stats:
                stat_name = s.stat["name"].replace("-", " ").upper()
                stats[stat_name] = s.base_stat

            # Format stats in a readable way
            stats_list = []
            for name, value in stats.items():
                stats_list.append(f"{name}: {value}")
            stats_str = "\n".join(stats_list)

        # Print everything
        print(separator)
        print(header)
        print(separator)
        print(f"Type: {types_str}")
        print(f"Height: {height_m:.1f} m")
        print(f"Weight: {weight_kg:.1f} kg")
        print(f"Abilities: {abilities_str}")

        if stats_str:
            print("\nBase Stats:")
            print(stats_str)

        # Print the ASCII sprite
        if ascii_sprite:
            print("\nSprite:")
            print(ascii_sprite)
        else:
            print("\nNo sprite available.")

        print(separator)
