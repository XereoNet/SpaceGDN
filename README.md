
This API uses [Semantic Versioning](http://semver.org/). The current version is 1.1.0-dev, developing towards 1.1.0.

#Version 1.1.0-dev
Version 1 of the API does not require any authentication to use. It is limited to a maximum of 1000 requests per hour per IP. If this maximum is exceeded, the API will return error 492 (in accordance with RFC 6585) in its errors (see below).

## Implementations

There have been several implementations of the SpaceGDN API in various languages:

 * **PHP**: [mcprohosting/spacegdn-bridge](https://github.com/MCProHosting/spacegdn-bridge)
 * **JavaScript**: [connor4312/spacegdn-bridge](https://github.com/connor4312/spacegdn-bridge)
 * **Python**: [totokaka/pySpaceGDN](https://github.com/totokaka/pySpaceGDN)

## Overview

Jars are layered by `Type > Channel > Version > Build`. For example, a standard Craftbukkit build could be chained as `Craftbukkit > Recommended > 1.6.4 > 1850`, for the last recommended build of version 1.6.4. The API is [RESTful](http://en.wikipedia.org/wiki/Representational_state_transfer) API. 

All requests to the API receive the following response format. `success` will either be set to true or false. `errors` will always be set, as an array of objects (see *Errors* below). In successful responses, `errors` will be empty. `results` will be the results of the query, and specified in the sections below. See the *Paginated Results* section for information on the pagination properties.

	{
		success: true|false,
		error: [],
		results: ...,
		pages: ...
	}

##Errors
Error are returned in the `error` property in each request response. Each error is an object consisting of two parts: a numeric error code (should be used for any internal testing) and a textual error message (for debugging or display). When an error occurs, a HTTP 400 code will be returned. The API may return the following errors:

 - `{ code: 492, message: 'API rate limit exceeded.' }` - This error is returned if the rate limit, 1000 requests per hour, is exceeded.
 - `{ code: 1000, message: 'Expecting digit, not "foo".' }` - This error is returned if a string was found in place of a digit, as would occur in the request `GET /jar/foo`, for example.
 - `{ code: 1001, message: 'Invalid hierarchy order of "foo". Parts must be given in the order of jar, channel, version, and build.' }` - This error is returned if request parts are given in the wrong order, like `GET /channel/2/jar`. This doesn't make sense, as "jars" own "channels", not the other way around.
 - `{ code: 1002, message: 'Invalid hierarchy part "foo". Must be one of jar, channel, version, or build.' }` - This error is returned if an invalid request part, such as "foo" is given in place of a resource.

##Resources

The following resources are available in this API:

 - `jar` - the type of jar, such as "Craftbukkit" or "FTB".
 - `channel` - channel of the jar or channel, such as "Recommended" or "MindCrack".
 - `version` - Minecraft version to correspond to, such as "1.6.2" or "1.7.2"
 - `build` - the jar build number, such as 1850.

> Note: some responses return a last updated time, created at time, etc. These are always the UTC Unix timestamp.

##Chaining

The data is hierarchical, so chaining may be done in the order of `Type > Channel > Version > Build`. For example, all of the following would be valid requests:

	GET /jar/:id/channel # Lists all channels for the given server jar
	GET /jar/:id/build # Jumps down the chain and lists builds for the given jar
	GET /channel/:id/build # Starts at the channel/channel, and lists all builds inside of it
	GET /jar/:id/channel/:id/version/:id/build # Verbosely gets all builds for the given version

##Bubbling
Bubbling was added in 1.0.1. Essentially, all requests will return the IDs of all their parents. For example, any `build` also returns the fields for `channel_id` and `jar_id`, as well as its own `version_id`.

##Sorting

Query results may be sorted, by appending a parameter to the URL in the following way format: `model.column.direction`.

 - `model` Must be one of: "jar", "channel", "version", "build"
 - `column` Must be a column on the model, as are returned in API requests.
 - `direction` Must be one of: "asc", "desc"

For example, a request like `GET /jar/1/build?sort=build.created_at.desc` returns builds, sorting by the newest added to the oldest. It's also worth noting that, with the "bubbling" added in version 1.0.1 of the API, it is possible to sort by any parent properties as well, such for example: `GET /jar/1/build?sort=jar.name.desc`

##Where
1.1.0-dev introduced the ability to run WHERE queries in the formation `model.column.operator.value`. For example:

	GET /v1/build?where=build.build.eq.2973

Retrieves the "build" with build number 2973. The parameters:

 - `model` Must be one of: "jar", "channel", "version", "build"
 - `column` Must be a column on the model, as are returned in API requests.
 - `operator` Must be one of:
   - `eq` Where column EQUALS the value
   - `lt` Where column is LESS THAN the value
   - `gt` Where column is GREATER THAN the value
   - `gteq` Where column is GREATER THAN or EQUAL TO the value
   - `lteq` Where column is LESS THAN or EQUAL TO the value
   - `in` Where the column is one of the "value", seperated by commas. For example: `build.build.in.2973,2972` gets build numbers 2973 *and* 2972
 - `value` The value to compare against.

##Paginated Results
In order to prevent flooding, results are paginated automatically to 100 results. Page information is always returned in the response object. Non-paginated results will simply display as having 1 page. Pages can be navigated to by passing the property `page` in the URL. For example:

	GET /jar/1/build?page=10

A page response object looks something like this. Properties are fairly self-explanitory:

	{
		pages: 42,
		has_next: true,
		has_prev: true,
		current_page: 8,
		total_items: 4244
	}

##Requests

###Type

The jar is the highest level in the hierarchy. The following requests are valid:

####Request
List all available jar jars:

	GET: /jar

#####Response
Returns an array of all jars available in the API. See the below request for contents of each jar object. Example:

	{
		success: true,
		error: {},
		results: [{ ... }, { ... }, { ... }, ...]
	}

#####Request
Show information on a single jar, by ID:

	GET: /jar/:id

#####Response
Example:

	{
		success: true,
		error: {},
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
		error: {},
		results: [{ ... }, { ... }, { ... }, ...]
	}

#####Request
Get information on a single channel, by ID:

	GET: /channel/:id

#####Response
Example:

	{
		success: true,
		error: {},
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
List all available versions. Note that versions may not be able to be resolved for some Jenkins sources, such as Bungeecord. In this case, version will be zero.

	GET: /version

#####Response

Example:

	{
		success: true,
		error: {},
		results: [{ ... }, { ... }, { ... }, ...]
	}

#####Request
Get information on a single channel, by ID:

	GET: /channel/:id

#####Response
Example:

	{
		success: true,
		error: {},
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
		error: {},
		results: [{ ... }, { ... }, { ... }, ...]
	}

#####Request
Get information on a single build, by ID:

	GET: /build/:id

#####Response

Currently the `checksum` and `size` properties are not available for Jenkins-based sources. You can use these if they are there, but don't depend upon them!

Example:

	{
		success: true,
		error: {},
		results: {
			'id': 1,
			'version_id': 1,
			'build': 1234,
			'size': 15295007,
			'checksum': '5c3d125265a806e842fe97625658fb1c',
			'url': 'http://dl.bukkit.org/downloads/craftbukkit/get/02389_1.6.4-R2.0/craftbukkit.jar',
			'created_at': 1384711375
		}
	}
