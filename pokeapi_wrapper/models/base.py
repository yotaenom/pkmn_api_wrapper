"""
Base models for the PokéAPI wrapper
"""

class NamedAPIResource:
    """
    Named API resource model
    
    This is used for resources that have a name and URL
    """
    def __init__(self, id=None, name=None, url=None, **kwargs):
        self.id = id
        self.name = name
        self.url = url

class VersionGameIndex:
    """
    Version game index model
    
    This is used for resources that have a game index in different versions
    """
    def __init__(self, game_index=None, version=None, **kwargs):
        self.game_index = game_index
        self.version = version

class PaginatedResponse:
    """
    Paginated response model
    
    This is used for endpoints that return a paginated list of resources
    """
    def __init__(self, count=0, next=None, previous=None, results=None):
        self.count = count
        self.next = next
        self.previous = previous
        self.results = results or [] 