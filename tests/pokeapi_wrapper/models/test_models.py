"""
Tests for the Pokemon models.
"""

import copy
from pokeapi_wrapper.models.pokemon import (
    Pokemon,
    PokemonAbility,
    PokemonType,
    PokemonSprites,
)

POKEMON_TEST_DATA = {
    "id": 25,
    "name": "pikachu",
    "height": 4,
    "weight": 60,
    "base_experience": 112,
    "types": [
        {
            "slot": 1,
            "type": {"name": "electric", "url": "https://pokeapi.co/api/v2/type/13/"},
        }
    ],
    "abilities": [
        {
            "ability": {
                "name": "static",
                "url": "https://pokeapi.co/api/v2/ability/9/",
            },
            "is_hidden": False,
            "slot": 1,
        },
        {
            "ability": {
                "name": "lightning-rod",
                "url": "https://pokeapi.co/api/v2/ability/31/",
            },
            "is_hidden": True,
            "slot": 3,
        },
    ],
    "stats": [
        {
            "base_stat": 35,
            "effort": 0,
            "stat": {"name": "hp", "url": "https://pokeapi.co/api/v2/stat/1/"},
        },
        {
            "base_stat": 55,
            "effort": 0,
            "stat": {"name": "attack", "url": "https://pokeapi.co/api/v2/stat/2/"},
        },
    ],
    "sprites": {
        "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png",
        "front_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/25.png",
        "back_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/25.png",
        "back_shiny": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/25.png",
    },
}


class TestPokemonModel:
    """Tests for the Pokemon model."""

    def test_init(self):
        """Test that the Pokemon class initializes correctly."""
        # Create a copy of the test data to avoid modifying the original
        pokemon_data = copy.deepcopy(POKEMON_TEST_DATA)

        # Initialize a Pokemon instance
        pokemon = Pokemon(**pokemon_data)

        # Check basic attributes
        assert pokemon.id == 25
        assert pokemon.name == "pikachu"
        assert pokemon.height == 4
        assert pokemon.weight == 60
        assert pokemon.base_experience == 112

        # Check nested objects
        assert len(pokemon.types) == 1
        assert isinstance(pokemon.types[0], PokemonType)
        assert pokemon.types[0].type["name"] == "electric"

        assert len(pokemon.abilities) == 2
        assert isinstance(pokemon.abilities[0], PokemonAbility)
        assert pokemon.abilities[0].ability["name"] == "static"
        assert pokemon.abilities[0].is_hidden is False
        assert pokemon.abilities[1].ability["name"] == "lightning-rod"
        assert pokemon.abilities[1].is_hidden is True

        assert len(pokemon.stats) == 2
        assert pokemon.stats[0].stat["name"] == "hp"
        assert pokemon.stats[0].base_stat == 35
        assert pokemon.stats[1].stat["name"] == "attack"
        assert pokemon.stats[1].base_stat == 55

        assert isinstance(pokemon.sprites, PokemonSprites)
        assert (
            pokemon.sprites.front_default
            == "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
        )
        assert (
            pokemon.sprites.front_shiny
            == "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/25.png"
        )
        assert (
            pokemon.sprites.back_default
            == "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/25.png"
        )
        assert (
            pokemon.sprites.back_shiny
            == "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/shiny/25.png"
        )

    def test_show_pokemon_method_exists(self):
        """Test that the show_pokemon method exists and has the correct signature."""
        # Create a Pokemon instance
        pokemon_data = copy.deepcopy(POKEMON_TEST_DATA)
        pokemon = Pokemon(**pokemon_data)

        # Check that the method exists
        assert hasattr(pokemon, "show_pokemon")

        # Check the method signature
        import inspect

        sig = inspect.signature(pokemon.show_pokemon)
        params = sig.parameters

        # Check that the method has the expected parameters with default values
        assert "colored" in params
        assert params["colored"].default is True


class TestPokemonAbility:
    """Tests for the PokemonAbility model."""

    def test_init(self):
        """Test that the PokemonAbility class initializes correctly."""
        ability_data = {
            "ability": {
                "name": "static",
                "url": "https://pokeapi.co/api/v2/ability/9/",
            },
            "is_hidden": False,
            "slot": 1,
        }

        ability = PokemonAbility(**ability_data)

        assert ability.ability["name"] == "static"
        assert ability.is_hidden is False
        assert ability.slot == 1


class TestPokemonType:
    """Tests for the PokemonType model."""

    def test_init(self):
        """Test that the PokemonType class initializes correctly."""
        type_data = {
            "slot": 1,
            "type": {"name": "electric", "url": "https://pokeapi.co/api/v2/type/13/"},
        }

        pokemon_type = PokemonType(**type_data)

        assert pokemon_type.type["name"] == "electric"
        assert pokemon_type.slot == 1


class TestPokemonSprites:
    """Tests for the PokemonSprites model."""

    def test_init(self):
        """Test that the PokemonSprites class initializes correctly."""
        sprites_data = {
            "front_default": "https://example.com/front.png",
            "front_shiny": "https://example.com/front_shiny.png",
            "back_default": "https://example.com/back.png",
            "back_shiny": "https://example.com/back_shiny.png",
        }

        sprites = PokemonSprites(**sprites_data)

        assert sprites.front_default == "https://example.com/front.png"
        assert sprites.front_shiny == "https://example.com/front_shiny.png"
        assert sprites.back_default == "https://example.com/back.png"
        assert sprites.back_shiny == "https://example.com/back_shiny.png"

        # Test default values for optional attributes
        assert sprites.front_female is None
        assert sprites.front_shiny_female is None
        assert sprites.back_female is None
        assert sprites.back_shiny_female is None
        assert sprites.other == {}
        assert sprites.versions == {}
