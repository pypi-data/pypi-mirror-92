Kraken-cache

Provides a caching mechanism for kraken records. 

from kraken_cache.kraken_cache import Kraken_cache

How to use:
Initialize cache at beginning. Load data from database with load method. Add data to be saved with set. Retrieve all of the data to be saved using export. Clear data to be saved (after a save to db) with clear_all. 



Initialize
k = Kraken_cache()

Store data (to be writtened to db)
k.set(id, data)

Load data (from db)
k.load(id, data)

Retrieve data
k.get(id)

Retrieve data that needs ot be saved to db
k.export()

Reset all data (after save to db)
k.clear_all()

