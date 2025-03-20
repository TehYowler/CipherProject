#Typing extras.
from typing import Iterable
from typing_extensions import Any;
from copy import copy;

#Sympy - A Python module for mathematical computation.
from sympy import Expr, Integer, symbols;
from sympy.abc import i, x
import sympy;

#Codeword operations for the Symbol Map Cipher
def lowered(inputArray: Iterable):
	seen = set()
	lowerCase = [char.lower() for char in inputArray if char.lower() not in seen and (seen.add(char.lower()) or True)];
	return lowerCase;
	#Credits to "https://www.geeksforgeeks.org/python-get-unique-values-list#using-list-comprehension" for the solution to get unique elements in order.

def uppered(inputArray: Iterable):
	seen = set()
	upperCase = [char.upper() for char in inputArray if char.upper() not in seen and (seen.add(char.upper()) or True)];
	return upperCase;
	#Credits to "https://www.geeksforgeeks.org/python-get-unique-values-list#using-list-comprehension" for the solution to get unique elements in order.

def bigraphic(inputArray: Iterable) -> list:
	poly = []
	for letter1 in inputArray:
		for letter2 in inputArray:
			poly.append(letter1 + letter2)
	return poly

def trigraphic(inputArray: Iterable) -> list:
	poly = []
	for letter1 in inputArray:
		for letter2 in inputArray:
			for letter3 in inputArray:
				poly.append(letter1 + letter2 + letter3)
	return poly

alphabet = [chr(num) for num in [*range(65,91), *range(97,123)]]

alphaNumeric = [chr(num) for num in [*range(48,58),*range(65,91), *range(97,123)]]

fullSet = [chr(num) for num in range(32,127)]
fullSet.append('\n');

#A custom exception for handling if a value is a single chracter or not.
class CharError(ValueError):
    def __init__(self, message):
        super().__init__(message);

#A custom exception for handling if a value is a string or not.
class StringError(TypeError):
    def __init__(self, message):
        super().__init__(message);

#A custom exception for handling if a value is a string or not.
class RangeError(TypeError):
    def __init__(self, message):
        super().__init__(message);

#A custom exception for handling if a value is a single chracter or not.
class NonIntegerError(TypeError):
    def __init__(self, message):
        super().__init__(message);

#A custom exception for handling if a value is a single chracter or not.
class EquationError(Exception):
    def __init__(self, message):
        super().__init__(message);

#A class of ciphering strings and chars based on Python's innate functions ord() and chr().
class AlgebraicCipher:
	allASCII = [chr(num) for num in range(178)]; #All ASCII characters in a list.

	#Constant messages.
	IS_EQUATION_ERROR = "Value is not an equation.";
	IS_INTEGER_ERROR = "Value is not an integer.";
	EQUATION_CORRECT_ERROR = "The given equation did not produce a number, please make sure to only use the x variable."
	RANGE_ERROR = f"This equation produces characters that go beyond the maximum or minimum 'chr' range of Python (0-{0x110000-1})";
	REVERSE_ERROR = "This equation could not be reversed - please use the x variable.";
	VARIABLE_ERROR = "Please only use the 'x' variable.";
	SIZE_ERROR = "This equation produces too large values.";
	STRING_ERROR = "A cipher input was not recognized as a string";
	CHAR_ERROR = "A cipher input was recognized as a string, but not recognized as a char.";
	SUCCESS = "This cipher worked!";
	UNKNOWN_ERROR = "An unknown error has occured, please try again.";

	@staticmethod
	def asEquation(equation: str|Expr) -> Expr:
		if(type(equation) == str):
			return sympy.S(equation);
		if(isinstance(equation,(Expr))):
			return equation;
		else:
			raise EquationError(AlgebraicCipher.IS_EQUATION_ERROR);

	@staticmethod
	def charCheck(check: Any) -> None:
		#Check a value to see if it is a chracter (length-1 string).
		if(type(check) != str):
			#If it is not a string, return a StringError.
			raise StringError(f"'{(check)}' instead of a string passed into AlgebraicCipher.encrypt.");

		if(len(check) != 1):
			#If it is not a char, return CharError.
			raise CharError(f"String of length {len(check)} instead of 1 passed into AlgebraicCipher.decrypt.");

		#Otherwise, nothing happens and code exeuction operates as normal.

	#Encrypt a single character.
	@staticmethod
	def encrypt(equation: str|Expr,char: str) -> str:
		AlgebraicCipher.charCheck(char); #Raise an error if "char" is not an appropriate character.
		eq = AlgebraicCipher.asEquation(equation); #If the equation is a string, convert the string into a proper equation object.
		ordinal = ord(char); #Get the ord of the character.

		#Evaluate "ordinal" as the ciphered integer of the char by passing the ord value into the equation.
		ordinal = eq.subs({x: ordinal });

		#If the number is sypmy's custom integer class, covnert to a normal integer.
		if isinstance(ordinal, Integer):
			ordinal = int(ordinal);

		#If somehow the result is not an integer, throw an errpr.
		if not isinstance(ordinal, (int)):
			raise NonIntegerError(AlgebraicCipher.IS_INTEGER_ERROR);

		if(not (0 <= ordinal <= 0x110000)):
			raise RangeError(AlgebraicCipher.RANGE_ERROR)

		return chr(ordinal); #If no error is thrown, return the corresponding letter to the shifted character.

	#Encrypt a whole string or iterable of characters.
	@staticmethod
	def encryptAll(equation: str|Expr,chars: str|Iterable[str]) -> str:
		eq = AlgebraicCipher.asEquation(equation);
		newString = ""; #Gets an empty string to append to.
		for char in chars:
			#Adds each encrypted character.
			newString += AlgebraicCipher.encrypt(eq,char);
		return newString; #Returns the bundled sequence as a string.

	#THe following decrypt methods practically act the same as the encrypt methods, except performing the reverse and swapping x for i.
	@staticmethod
	def decrypt(equation: str|Expr,char) -> str:
		AlgebraicCipher.charCheck(char);
		eq = AlgebraicCipher.asEquation(equation);
		inverse = sympy.S(sympy.solve(eq - i, x))[0];
		ordinal = ord(char);

		ordinal = inverse.subs({i: ordinal });

		if isinstance(ordinal, Integer):
			ordinal = int(ordinal);

		if not isinstance(ordinal, int):
			raise NonIntegerError(AlgebraicCipher.IS_INTEGER_ERROR);
		return chr(ordinal);

	@staticmethod
	def decryptAll(equation: str|Expr,chars: str|Iterable[str]) -> str:
		eq = AlgebraicCipher.asEquation(equation);
		newString = "";
		for char in chars:
			newString += AlgebraicCipher.decrypt(eq,char);
		return newString;

	#Checks if encryption is possible, and returns a result if it is.
	@staticmethod
	def encryptPossible(equation: str|Expr, chars: str|Iterable[str] = allASCII) -> str:
		#Performs an encryption check on the used characters, which defaults to all ASCII characters.
		#Then, returns a constant string depending on the result.

		try:
			AlgebraicCipher.encryptAll(equation,chars);
			AlgebraicCipher.decryptAll(equation, AlgebraicCipher.encryptAll(equation,chars));
			return AlgebraicCipher.SUCCESS; #If no errors happen to this point, return a success.
		#Otherwise, of the many error cases, return a massge corresponding to that error case.
		except StringError as error:
			return AlgebraicCipher.STRING_ERROR;
		except CharError as error:
			return AlgebraicCipher.CHAR_ERROR;
		except EquationError as error:
			return AlgebraicCipher.IS_EQUATION_ERROR;
		except OverflowError as error:
			return AlgebraicCipher.SIZE_ERROR;
		except NonIntegerError as error:
			return AlgebraicCipher.EQUATION_CORRECT_ERROR;
		except RangeError as error:
			return AlgebraicCipher.RANGE_ERROR;
		except Exception:
			return AlgebraicCipher.UNKNOWN_ERROR;


	#Same as encryptPossible, except for decryption.
	@staticmethod
	def decryptPossible(equation: str|Expr, chars: str|Iterable[str] = allASCII) -> str:

		try:
			AlgebraicCipher.decryptAll(equation,chars);
			AlgebraicCipher.encryptAll(equation, AlgebraicCipher.decryptAll(equation,chars));
			return AlgebraicCipher.SUCCESS;
		except StringError as error:
			return AlgebraicCipher.STRING_ERROR;
		except CharError as error:
			return AlgebraicCipher.CHAR_ERROR;
		except EquationError as error:
			return AlgebraicCipher.IS_EQUATION_ERROR;
		except NonIntegerError as error:
			return AlgebraicCipher.EQUATION_CORRECT_ERROR;
		except OverflowError as error:
			return AlgebraicCipher.SIZE_ERROR;
		except RangeError as error:
			return AlgebraicCipher.RANGE_ERROR;
		except Exception:
			return AlgebraicCipher.UNKNOWN_ERROR;

def caesarCipher(string: str,key: int):
	key %= 26;
	if(key == 0): #If there is no shift, then just return the original string.
		return string;

	#Initialize string to add to for the cipher.
	returnString = "";

	for char in string:
		#If the character is lowercase, cipher its lowercase variant.
		if( char in lowered(alphabet) ):
			index = lowered(alphabet).index(char);
			index += key;
			index %= 26;
			returnString += lowered(alphabet)[index];
		#If the character is uppercase, cipher its lowercase variant.
		elif( char in uppered(alphabet) ):
			index = uppered(alphabet).index(char);
			index += key;
			index %= 26;
			returnString += uppered(alphabet)[index];
		#For all other cases like spaces or punctuation, ignore any special operations and just add it to the string.
		else:
			returnString += char
	return returnString

def codePointCaesarCipher(string: str,shift: int, lower:int|None=None ,upper:int|None=None ):

	if(shift == 0): #If there is no shift, jsut return the same string.
		return string;

	if(lower is None or upper is None):
		lower = 0x110000;
		upper = 0;
		for char in string:
			order = ord(char)
			lower = min(lower,order);
			upper = max(upper,order);
	if(shift % (upper - lower + 1) == 0): #If the shift would result in the same string, jsut return the same string.
		return string;

	returnString = "";

	for char in string:
		order = ord(char)
		order += shift;
		order -= lower;
		order %= upper - lower + 1;
		order += lower;
		returnString += chr(order);

	return returnString;

def inPlaceCaesarCipher(string: str,shift: int):

	if(shift == 0): #If there is no shift, jsut return the same string.
		return string;

	seen = set()
	orderArray = [ord(char) for char in string if char not in seen and (seen.add(char) or True)];
	orderArray.sort();

	shift %= len(orderArray);

	postOrderArray = copy(orderArray);
	for times in range(shift):
		postOrderArray.insert(0,postOrderArray.pop());

	returnString = "";

	for char in string:
		order = ord(char);
		index = orderArray.index(order);
		returnString += chr(postOrderArray[index]);


	return returnString;

if(__name__ == "__main__"): #Demo if the file is run directly.

	print("Caesar cipher for 'This is a cat.', shifting right one:")
	print(caesarCipher("This is a cat.",1))
	print()

	print("Caesar cipher for 'This is a cat.', shifting left ten times:")
	print(caesarCipher("This is a cat.",-10))
	print()

	print("Code point cipher for 'This is a cat.', shifting right one:")
	print(codePointCaesarCipher("This is a cat.",1))
	print()

	print("Code point cipher for 'This is a cat.', shifting left one:")
	print(codePointCaesarCipher("This is a cat.",-1))
	print()

	print("Code point cipher for 'abcdABCD', shifting right five times:")
	print(codePointCaesarCipher("abcdABCD",5))
	print()

	print("In-place cipher for 'This is a cat.', shifting right once:")
	print(inPlaceCaesarCipher("This is a cat.",1))
	print()

	print("In-place cipher for 'This is a cat.', shifting left once:")
	print(inPlaceCaesarCipher("This is a cat.",-1))
	print()

	print("In-place cipher for 'acdAAABCDDD', shifting right two times:")
	print(inPlaceCaesarCipher("acdAAABCDDD",2))
	print()

	print("In-place cipher for 'acdAAABCDDD', shifting left once:")
	print(inPlaceCaesarCipher("acdAAABCDDD",-1))
	print()

	print("Below is the input for the AlgebraicCipher class.")

	while(True):

		#For clearing the screen.
		import os;
		clear = lambda: os.system('cls' if os.name == 'nt' else 'clear'); #Multi-system terminal clear capability/

		#The string to encrypt or decrypt.
		string = input("Input a user string to cipher. This uses the AlgebraicCipher class. Type 'cancel' to exit the program. ");

		if(not string):
			clear();
			print('Please enter a non-empty string.')
			continue;

		if(string == "cancel"): #Exits at will.
			break;

		#Gets and shows the user the ordinal range of the string to get an idea of how not to go over the pre-determined chr range.
		lowestOrd = 0;
		highestOrd = 0;

		for char in string:
			lowestOrd = min(ord(char),lowestOrd);
			highestOrd = max(ord(char),highestOrd);
		print(f"The ord values of this string range from {lowestOrd}-{highestOrd}.");
		print();

		print("Type 'c' to encrypt, and 'd' to decrypt.")
		while(True):
			#Waits for the user to type c or d, otherwise ask to try again.
			typeCipher = input("");
			print();

			if(typeCipher != 'd' and typeCipher != 'c'):
				print("Please try again.")
				continue;
			break;

		#AlgebraicCipher the string with the equation.
		if(typeCipher == 'c'):

			#Get the equation first.
			equation = input(f"Input an equation to use on the string, in terms of x.\nThe equation should should produce either 0 or positive values less than {0x110000}. ");
			isPossible = AlgebraicCipher.encryptPossible(equation,string); #Then determines if it is possible.

			#If the equation and string cannot work together, say so and reset the loop via 'continue'.
			if(isPossible != AlgebraicCipher.SUCCESS):
				clear();
				print(isPossible);
				continue;

			#Otherwise, encrypt the string and show the result.
			ciphered = AlgebraicCipher.encryptAll(equation,string);

			clear();
			print('Ciphered string: ')
			print(ciphered)
			print();

			unciphered = AlgebraicCipher.decryptAll(equation,ciphered);

			print('Deciphered string (reversed process): ')
			print(unciphered);

		#Otherwise, decrypt, effectively the same as encrypting but with the opposite methods.
		else:
			equation = input(f"Input the equation used to initially encrypt the string. ");
			isPossible = AlgebraicCipher.decryptPossible(equation,string);
			if(isPossible != AlgebraicCipher.SUCCESS):
				clear();
				print(isPossible);
				continue;

			unciphered = AlgebraicCipher.decryptAll(equation,string);

			clear();
			print('Unciphered string: ')
			print(unciphered)
			print();

			ciphered = AlgebraicCipher.encryptAll(equation,unciphered);

			print('Ciphered string (reversed process): ')
			print(ciphered);
