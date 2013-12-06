from gdn.v1 import lang

def build(parts):

	valid_parts = ['type', 'channel', 'version', 'build']
	heirarchy_pointer = -1
	expecting_id = False

	data = {}
	
	for seg, part in enumerate(parts):
		if expecting_id:
			if part.isdigit():
				data[parts[seg - 1]] = part
				expecting_id = False
				continue
			else:
				raise Exception(lang.invalid_digit % part)

		point = -1
		for index, check in enumerate(valid_parts):
			if check == part:
				point = index
				break

		if point == -1:
			raise Exception(lang.invalid_part % part)

		if point <= heirarchy_pointer:
			raise Exception(lang.invalid_order % part)

		heirarchy_pointer = point
		expecting_id = True

	if expecting_id:
		select = parts[len(parts) - 1]
	else:
		select = parts[len(parts) - 2]

	return {
		'select': select,
		'data': data
	}