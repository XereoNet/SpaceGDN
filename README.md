
This API uses [Semantic Versioning](http://semver.org/). The current version is 0.0.0, developing towards 0.1.0.

#Version 1.0.0
Version 1 of the API does not require any authentication to use. It is limited to a maximum of 1000 requests per hour per IP. If this maximum is exceeded, the API will return error 492 (in accordance with RFC 6585) in its errors (see below).

Jars are layered by `Type > Channel > Version > Build`. For example, a standard Craftbukkit build could be chained as `Craftbukkit > Recommended > 1.6.4 > 1850`, for the last recommended build of version 1.6.4. The API is [RESTful](http://en.wikipedia.org/wiki/Representational_state_transfer) API. 

All requests to the API receive the following response format. `success` will either be set to true or false. `errors` will always be set, as an array of objects (see *Errors* below). In successful responses, `errors` will be empty. `results` will be the results of the query, and specified in the sections below. See the *Paginated Results* section for information on the pagination properties.

	{
		success: true|false,
		errors: [],
		results: ...,
		pages: ...
	}

##Errors
Errors are returned in the `errors` array in each request response. Each error is an object consisting of two parts: a numeric error code (should be used for any internal testing) and a textual error message (for debugging or display). The API may return the following errors:

 - `{ code: 492, message: 'API rate limit exceeded }` - This error is returned if the rate limit, 1000 requests per hour, is exceeded.

##Resources

The following resources are available in this API:

 - `type` - the type of jar, such as "Craftbukkit" or "FTB".
 - `channel` - channel of the jar or channel, such as "Recommended" or "MindCrack".
 - `version` - Minecraft version to correspond to, such as "1.6.2" or "1.7.2"
 - `build` - the jar build number, such as 1850.

> Note: some responses return a last updated time, created at time, etc. These are always the UTC Unix timestamp.

##Chaining

The data is hierarchical, so chaining may be done in the order of `Type > Channel > Version > Build`. For example, all of the following would be valid requests:

	GET /type/:id/channel # Lists all channels/channels for the given server type
	GET /type/:id/build # Jumps down the chain and lists builds for the given type
	GET /channel/:id/build # Starts at the channel/channel, and lists all builds inside of it
	GET /type/:id/channel/:id/version/:id/build # Verbosely gets all builds for the given version

##Modifiers

You may also note that you can apply the following modifiers to your query, to adjust the results:

 - Order by:
 	- `order_by` - Sets the column to order the results by.
 	- `order_dir` - Sets the direction, ASCending or DESCending, to show the results by.
 - Where:
    - `where_value` the value to check, such as `last_updated`.
    - `where_is` the value to check against.
 	- `where_op` sets the operator to use in the where query. Defaults to `=` if not given.

To tie this all together, let's say I wanted to get all updates for the jar type with "id" of 1 since the Unix time 1384711375. I would make the following request. Note that I have not URL encoded the parameters for readability, though I would have to in order to actually make a request.

	GET /type/1/build?order_by=last_updated&order_dir=DESC&where_value=last_updated&where_op=>&where_is=1384711375

##Paginated Results
In order to prevent flooding, results are paginated automatically to 100 results. The number of pages is always returned in the response object (see above). Non-paginated results will simply display as having 1 page. Pages can be navigated to by passing the property `page` in the URL. For example:

	GET /type/1/build?page=10

##Requests

###Type

The jar type is the highest level in the hierarchy. The following requests are valid:

####Request
List all available jar types:

	GET: /type

#####Response
Returns an array of all jars available in the API. See the below request for contents of each jar object. Example:

	{
		success: true,
		errors: [],
		results: [{ ... }, { ... }, { ... }, ...]
	}

#####Request
Show information on a single jar type, by ID:

	GET: /type/:id

#####Response
Example:

	{
		success: true,
		errors: [],
		results: {
			'id': 1,
			'name': 'Craftbukkit',
			'site_url': 'http://bukkit.org',
			'updated_at': 1384711375
		}
	}

###Channel

Request for jar channels.

#####Request
List all available channels.

	GET: /channel

#####Response
Example:

	{
		success: true,
		errors: [],
		results: [{ ... }, { ... }, { ... }, ...]
	}

#####Request
Get information on a single channel, by ID:

	GET: /channel/:id

#####Response
Example:

	{
		success: true,
		errors: [],
		results: {
			'id': 1,
			'name': 'Recommended',
			'jar_id': 1,
			'updated_at': 1384711375
		}
	}

###Version

Request for versions.

#####Request
List all available versions.

	GET: /version

#####Response
Example:

	{
		success: true,
		errors: [],
		results: [{ ... }, { ... }, { ... }, ...]
	}

#####Request
Get information on a single channel, by ID:

	GET: /channel/:id

#####Response
Example:

	{
		success: true,
		errors: [],
		results: {
			'id': 1,
			'version': '1.6.4',
			'name_id': 1,
			'updated_at': 1384711375
		}
	}

###Build

Request for all builds in a channel.

#####Request
List all available builds.

	GET: /build

#####Response
Example:

	{
		success: true,
		errors: [],
		results: [{ ... }, { ... }, { ... }, ...]
	}

#####Request
Get information on a single build, by ID:

	GET: /build/:id

#####Response
Example:

	{
		success: true,
		errors: [],
		results: {
			'id': 1,
			'version_id': 1,
			'build': 1234,
			'downloads': 1234,
			'size': 15295007,
			'checksum': '5c3d125265a806e842fe97625658fb1c',
			'url': 'http://dl.bukkit.org/downloads/craftbukkit/get/02389_1.6.4-R2.0/craftbukkit.jar',
			'created_at': 1384711375
		}
	}
