# Original function by http://joncom.be/code/javascript-json-formatter/

RealTypeOf = (v) ->
	if typeof (v) is "object"
		return "null"	if v is null
		return "array"	if v.constructor is (new Array).constructor
		return "date"	if v.constructor is (new Date).constructor
		return "regex"	if v.constructor is (new RegExp).constructor
		return "object"
	typeof (v)

formatJSON = (oData, sIndent = "") ->
	sIndentStyle = "		"
	sDataType = RealTypeOf(oData)
	
	# open object
	if sDataType is "array"
		return "[]"	if oData.length is 0
		sHTML = "["
	else
		iCount = Object.keys(oData).length
		
		return "{}"	if iCount is 0
		sHTML = "{"
	
	# loop through items
	iCount = 0
	each = (data, callback) ->
		if RealTypeOf(data) is "array"
			callback(key, value) for value, key in data
		else if RealTypeOf(data) is "object"
			callback(key, value) for key, value of data

	each oData, (sKey, vValue) ->
		sHTML += ","	if iCount > 0
		if sDataType is "array"
			sHTML += ("\n" + sIndent + sIndentStyle)
		else
			sHTML += ("\n" + sIndent + sIndentStyle + "\"" + sKey + "\"" + ": ")
		
		# display relevant data type
		switch RealTypeOf(vValue)
			when "array", "object"
				sHTML += formatJSON(vValue, (sIndent + sIndentStyle))
			when "boolean", "number"
				sHTML += vValue.toString()
			when "null"
				sHTML += "null"
			when "string"
				sHTML += ("\"" + vValue + "\"")
			else
				sHTML += ("TYPEOF: " + typeof (vValue))
		
		# loopƒ
		iCount++

	
	# close object
	if sDataType is "array"
		sHTML += "\n" + sIndent + "]"
	else
		sHTML += "\n" + sIndent + "}"
	
	# return
	return sHTML

elem = document.getElementById("js-code")
elem.innerHTML = formatJSON(JSON.parse(elem.innerHTML))
