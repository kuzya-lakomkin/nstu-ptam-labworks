from temp_parser import *
from utils import *

VERSION = "0.1"

def app():
	cnt = 0
	res = 0
	curr_val = (0, None)

	print(f"\n  ~~~~~~~~~~~~~~ Temperature Parser v{VERSION} ~~~~~~~~~~~~~~  \n\n"
	   		"Expected input format:\n<float number> [ \"K\" | \"F\" | \"C\" ] ... "\
            " <float number> [ \"K\" | \"F\" | \"C\" ]\n")
	print("Enter the temperature list: ")
	parser = ParserFSM()
	

	while len(curr_val) == 2:
		try:
			curr_val = parser.parse()
		except TempParserException as e:
			raise e

		if (len(curr_val) != 2):
			break
		
		celsium = convert_temp(curr_val)
		if (celsium < MIN_TEMP) or (celsium > MAX_TEMP):
			raise WrongTempException(curr_val[0], curr_val[1])
		
		res += g_float(celsium, .0)
		cnt += 1
	
	if cnt != 31:
		raise MissingValueException(cnt)
	
	print(f"\nTotal count of days, when weather was greater then 0.0 C: {res}")
 

if __name__ == '__main__':
	try:
		app()
	except TempParserException as e:
		print(e.args[0])
