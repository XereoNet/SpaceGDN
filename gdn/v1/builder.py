from gdn.v1 import lang

def build(parts):

	valid_parts = ['type', 'channel', 'version', 'build']
	heirarchy_pointer = 0
	expecting_id = False

	data = {}
	print parts
	for seg, part in enumerate(parts):
		if expecting_id:
			if part.isdigit():
				data[seg - 1] = part
				expecting_id = False
				continue
			else:
				return lang.invalid_digit % part, 400

		point = -1
		for index, check in enumerate(valid_parts):
			if check == part:
				point = index
				break

		if point == -1:
			return lang.invalid_part % part, 400

		if point <= heirarchy_pointer:
			return lang.invalid_order % part, 400

		expecting_id = True

	if expecting_id:
		select = parts[len(parts) - 1]
	else:
		select = parts[len(parts) - 2]

	return {
		'select': select,
		'data': data
	}