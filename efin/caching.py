import requests_cache

def initialize_cache(expire_after=3600):
    """
    Initialize a cache for HTTP requests (default expiration: 1 hour).
    """
    requests_cache.install_cache('efin_cache', expire_after=expire_after)

#Call initialize_cache() at the start of your scripts or in the package's main initialization.

