 developing a storage web application with an in-memory key-value memory cache.
 using Python and the Flask framework
 
A web front end that provides the following functionalities:
A page to upload a new pair of key and image: the key should be used to uniquely identify its image. A subsequent upload with the same key will replace the image stored previously. The web front end should store the image in the local file system, and add the key to the list of known keys in the database. Upon an update, the mem-cache entry with this key should be invalidated.
A page that shows an image associated with a given key.
A page that displays all the available keys stored in the database.
A page to configure the mem-cache parameters (e.g., capacity in MB, replacement policy) as well as clear the cache. 
Display a page with the current statistics for the mem-cache over the past 10 minutes.

Key-Value Memory Cache: a mem-cache is an in-memory cache that should be implemented as a Flask-based application. The mem-cache should be able to support these operations:
PUT(key, value) to set the key and value (contents of the image).
GET(key) to get the content associated with the key.
CLEAR() to drop all keys and values.
invalidateKey(key) to drop a specific key.
refreshConfiguration() to read mem-cache related details from the database and reconfigure it based on the values set by the user 

The mem-cache should support two cache replacement policies:
Random Replacement: Randomly selects a key and discards it to make space when necessary. This algorithm does not require keeping any information about the access history.
Least Recently Used: Discards the least recently used keys first. This algorithm requires keeping track of what was used when, if one wants to make sure the algorithm always discards the least recently used key.
