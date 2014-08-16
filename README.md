
This API uses [Semantic Versioning](http://semver.org/). The current version is 2.0.0-dev, developing towards 2.0.0. It is *not* backwards compatible with previous versions of the API.

#Version 2.0.0-dev
Version 2 of the API does not require any authentication to use. It is limited to a maximum of 1000 requests per hour per IP. If this maximum is exceeded, the API will return error 492 (in accordance with RFC 6585) in its errors (see below).

## Implementations

There have been several implementations of the SpaceGDN API in various languages:

#### Version 1-compatible clients:

 * **PHP**: [mcprohosting/spacegdn-bridge](https://github.com/MCProHosting/spacegdn-bridge)
 * **JavaScript**: [connor4312/spacegdn-bridge](https://github.com/connor4312/spacegdn-bridge)
 * **Python**: [totokaka/pySpaceGDN](https://github.com/totokaka/pySpaceGDN)
 * **Java**: [boboman13/SpaceGDN-Java](https://github.com/boboman13/SpaceGDN-Java)

## Overview

Version 2 of the GDN has an arbitrary heirarchy of data, allowing for significantly greater flexiblity of data. However, there are the following guarentees:

 * There will always be a top-level heirarchy `game`
   * In the game `minecraft` there will always be the following heirarchy parts: `type > version > build`

These are not the *only* heirarchy parts which may be present, but these are the parts which always exist. They can be queried in a standard route format.
 
 * The first part of the route must be `v2`
 * There may be zero or more parent IDs following `v2`
 * The resource type to get can be specified in the GET parameter `r`. If not passed, all possible resources will be returned.

Examples:

```
Returns all games, with "game" being the resource and no parents given:
    /v2/?r=game

Returns all "types" of the the game "minecraft", using Minecraft as the parent ID.
    /v2/minecraft/?r=type               

Returns all versions for "craftbukkit" which is a child of "minecraft".
    /v2/minecraft/craftbukkit/?r=version

This is the same as the above request. IDs are globally unique.
    /v2/craftbukkit?r=version

This gets *all* resource types which have Craftbukkit as a parent at
any point. This would return a mix of versions and builds.
    /v2/craftbukkit
```

##Errors
The only errors which is intentionally returned is HTTP code `492` and `400` (with a blank response), indicating a malformed request or that the rate limit is exceeded, respectively. 

##Bubbling
All response objects will return the IDs of all their parents in an array of zero or more strings "parents". For example:

```json
{
    "id": "SomeID",
    "version": "3.1.2",
    "parents": ["minecraft", "craftbukkit"],
    "created_at": "Sun, 10 Aug 2014 19:34:09 GMT"
}
```

If `parents=true` is passed as a GET parameter to the request, it will return each parent's data as a property, with the parent *type* being the key. Passing the parent will restrict the result to the first matching record. For example, a response might look like:

```json
{
    "id": "SomeID",
    "version": "3.1.2",
    "game": {
        "id": "minecraft",
        "name": "Minecraft",
        "created_at": "Sun, 10 Aug 2014 19:39:58 GMT",
        "updated_at": "Sun, 10 Aug 2014 19:39:59 GMT"
    },
    "type": {
        "id": "craftbukkit",
        "description": "CraftBukkit is The Minecraft Server Mod API Implementation.",
        "name": "CraftBukkit",
        "site_url": "http://dl.bukkit.org/downloads/craftbukkit/",
        "created_at": "Sun, 10 Aug 2014 19:39:58 GMT",
        "updated_at": "Sun, 10 Aug 2014 19:39:59 GMT"
    },
    "created_at": "Sun, 10 Aug 2014 19:34:09 GMT"
}
```

##Sorting

Query results may be sorted, by appending a parameter to the URL in the following way format: `key.direction`.

 - `key` Must be a property on the model, as are returned in API requests.
 - `direction` Must be one of: "asc", "desc"

Multiple sortings are possible by using a `|` as delimiter between `key.direction` pairs.

For example, a request like `GET /v2/minecraft?r=version&sort=version.desc|created_at.desc` returns builds, sorting primarily by version and by created\_at where versions are the same.

##Where
It is possible to filter results using the formation `property.operator.value`. Like sorting, it may also be delimited by `|` for multiple clauses. For example:

	GET /v2/?r=build&where=build.$gt.2973

Retrieves the "build" with build number above 2973. The parameters:

 - `property` Must be a property which exists on the resource you are querying.
 - `operator` may be any [Mongo comparison operator](http://docs.mongodb.org/manual/reference/operator/query/#comparison) or "$eq" to compare equality.
 - `value` The value to compare against. Arrays may be indicated (if you want to query with `$in` or `$nin`) by delimitation with commas.

##Paginated Results
In order to prevent flooding, results are paginated automatically to 100 results. Page information is always returned in the response object. Non-paginated results will simply display as having 1 page. Pages can be navigated to by passing the property `page` in the URL. For example:

    GET /jar/1/build?page=10

Note that, due to the Mongo constraints, there is not a way to determine the size of a result set without examining every item in the set. Therefore, the `has_next` in the pagination is set to `true` if the number of items is equal to the total the application is set to display per page. Meaning that, in some rare cases, `has_next` might be true on the "last" page of a collection. Do not depend on the result set having more than zero elements.

## General Response Format

```js
{
  "pagination": {
    "page": 1,              // The current page requested. Will be equal to "1" or the "page" given as a GET param.
    "per_page": 100         // The number of items displayed per page.
    "has_next": true,       // True if there are pages after the current page
    "has_prev": false,      // True if there are pages before the current page
  },
  "results": [ /* ... */ ]  // An array of results objects
}
```
