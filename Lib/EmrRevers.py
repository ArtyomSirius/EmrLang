def get():
	code = ["""
	init "isOBJ"
	func revers(data) { 
		#REVERS for EMERALD 1.0
		if isStr(data) {
			var index = -1 
			var len = len(data) 
			var result = "" 
			for i=0 to data { 
				var result = result + (data / index) 
				var index = index + -1 
			} 
			return result 
		} elif isList(data) {
			var index = -1 
			var len = len(data)
			var result = []
			for i=0 to data { 
				append(result, (data / index))
				var index = index + -1
			}
			return result
		} else {
			TraceBack("Argument must be a string or list!")
		}
	}
	"""]
	return code