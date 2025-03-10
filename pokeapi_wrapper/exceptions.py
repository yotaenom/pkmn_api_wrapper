"""
Exceptions for the PokéAPI wrapper
"""

class PokeAPIError(Exception):
    """Base exception for PokéAPI errors"""
    pass

class ResourceNotFoundError(PokeAPIError):
    """Exception raised when a resource is not found"""
    pass

class InvalidParameterError(PokeAPIError):
    """Exception raised when an invalid parameter is provided"""
    pass

class RateLimitError(PokeAPIError):
    """Exception raised when the API rate limit is exceeded"""
    pass

class NetworkError(PokeAPIError):
    """Exception raised when there's a network error"""
    pass

class ParsingError(PokeAPIError):
    """Exception raised when there's an error parsing the API response"""
    pass 