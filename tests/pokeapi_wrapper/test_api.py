"""
Tests for the PokeAPI client.
"""

import pytest
from pokeapi_wrapper.api import PokeAPI
from pokeapi_wrapper.exceptions import ResourceNotFoundError


class TestPokeAPI:
    """Tests for the PokeAPI class."""

    def test_get_pokemon_integration(self):
        """
        Integration test for get_pokemon.

        This test makes a real API call to the PokeAPI, so it's skipped by default.
        To run this test, use: pytest tests/test_api.py::TestPokeAPI::test_get_pokemon_integration -v
        """
        api = PokeAPI()
        pokemon = api.get_pokemon("pikachu")

        # Basic checks
        assert pokemon.name == "pikachu"
        assert pokemon.id == 25
        assert len(pokemon.types) > 0
        assert len(pokemon.abilities) > 0

    def test_get_pokemon_list_integration(self):
        """
        Integration test for get_pokemon_list.

        This test makes a real API call to the PokeAPI, so it's skipped by default.
        To run this test, use: pytest tests/test_api.py::TestPokeAPI::test_get_pokemon_list_integration -v
        """
        api = PokeAPI()
        pokemon_list = api.get_pokemon_list(limit=5)

        # Basic checks
        assert pokemon_list.count > 0
        assert len(pokemon_list.results) == 5

    def test_get_pokemon_not_found_integration(self):
        """
        Integration test for get_pokemon with a non-existent Pokemon.

        This test makes a real API call to the PokeAPI, so it's skipped by default.
        To run this test, use: pytest tests/test_api.py::TestPokeAPI::test_get_pokemon_not_found_integration -v
        """
        api = PokeAPI()

        # This should raise a ResourceNotFoundError
        with pytest.raises(ResourceNotFoundError):
            api.get_pokemon("not-a-pokemon")
