"""
Main API client for the PokéAPI wrapper
"""

import requests
import logging
from urllib.parse import urljoin

from .models.pokemon import Pokemon
from .models.base import PaginatedResponse
from .exceptions import PokeAPIError, ResourceNotFoundError


class PokeAPI:
    """
    Main client for the PokéAPI wrapper
    """

    BASE_URL = "https://pokeapi.co/api/v2/"

    def __init__(self):
        """
        Initialize the PokéAPI client
        """
        self.logger = logging.getLogger("pokeapi_wrapper")

    def _make_request(self, endpoint, params=None):
        """
        Make a request to the PokéAPI

        Args:
            endpoint: API endpoint to request
            params: Query parameters

        Returns:
            JSON response as dictionary

        Raises:
            ResourceNotFoundError: If the resource is not found
            PokeAPIError: If there's an error with the API request
        """
        url = urljoin(self.BASE_URL, endpoint)

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                raise ResourceNotFoundError(f"Resource not found: {endpoint}")
            else:
                raise PokeAPIError(f"HTTP Error: {e}")
        except requests.exceptions.RequestException as e:
            raise PokeAPIError(f"Request Error: {e}")
        except ValueError as e:
            raise PokeAPIError(f"Invalid JSON response: {e}")

    def _get_resource(self, resource_type, identifier):
        """
        Get a resource by its identifier

        Args:
            resource_type: Type of resource (e.g., 'pokemon')
            identifier: Name or ID of the resource

        Returns:
            JSON response as dictionary
        """
        endpoint = f"{resource_type}/{identifier}"
        return self._make_request(endpoint)

    def _get_resource_list(self, resource_type, limit=20, offset=0):
        """
        Get a paginated list of resources

        Args:
            resource_type: Type of resource (e.g., 'pokemon')
            limit: Number of results to return
            offset: Offset for pagination

        Returns:
            PaginatedResponse containing the results
        """
        params = {"limit": limit, "offset": offset}
        data = self._make_request(resource_type, params)

        # Create a new PaginatedResponse
        paginated_response = PaginatedResponse(
            count=data.get("count", 0),
            next=data.get("next"),
            previous=data.get("previous"),
            results=[],
        )

        # Convert the results to the appropriate model
        for item in data.get("results", []):
            # Extract ID from URL
            url_parts = item["url"].rstrip("/").split("/")
            item_id = int(url_parts[-1])

            # Create a simple dict with the necessary data
            item_data = {"id": item_id, "name": item["name"], "url": item["url"]}

            # For the list view, we don't need to parse the full model
            # Just create a simple object with id, name, and url
            paginated_response.results.append(item_data)

        return paginated_response

    # Pokemon endpoints
    def get_pokemon(self, identifier):
        """Get a Pokemon by name or ID"""
        pokemon_data = self._get_resource("pokemon", identifier)
        return Pokemon(**pokemon_data)

    def get_pokemon_list(self, limit=20, offset=0):
        """Get a list of Pokemon"""
        return self._get_resource_list("pokemon", limit, offset)
