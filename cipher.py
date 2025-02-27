#Typing extras.
from typing import Iterable
from typing_extensions import Any;

#Sympy - A Python module for mathematical computation.
from sympy import Expr, Integer, symbols;
from sympy.abc import i, x
import sympy;

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
class Cipher:
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
			raise EquationError(Cipher.IS_EQUATION_ERROR);

	@staticmethod
	def charCheck(check: Any) -> None:
		#Check a value to see if it is a chracter (length-1 string).
		if(type(check) != str):
			#If it is not a string, return a StringError.
			raise StringError(f"'{(check)}' instead of a string passed into Cipher.encrypt.");

		if(len(check) != 1):
			#If it is not a char, return CharError.
			raise CharError(f"String of length {len(check)} instead of 1 passed into Cipher.decrypt.");

		#Otherwise, nothing happens and code exeuction operates as normal.

	#Encrypt a single character.
	@staticmethod
	def encrypt(equation: str|Expr,char: str) -> str:
		Cipher.charCheck(char); #Raise an error if "char" is not an appropriate character.
		eq = Cipher.asEquation(equation); #If the equation is a string, convert the string into a proper equation object.
		ordinal = ord(char); #Get the ord of the character.

		#Evaluate "ordinal" as the ciphered integer of the char by passing the ord value into the equation.
		ordinal = eq.subs({x: ordinal });

		#If the number is sypmy's custom integer class, covnert to a normal integer.
		if isinstance(ordinal, Integer):
			ordinal = int(ordinal);

		#If somehow the result is not an integer, throw an errpr.
		if not isinstance(ordinal, (int)):
			raise NonIntegerError(Cipher.IS_INTEGER_ERROR);

		if(not (0 <= ordinal <= 0x110000)):
			raise RangeError(Cipher.RANGE_ERROR)

		return chr(ordinal); #If no error is thrown, return the corresponding letter to the shifted character.

	#Encrypt a whole string or iterable of characters.
	@staticmethod
	def encryptAll(equation: str|Expr,chars: str|Iterable[str]) -> str:
		eq = Cipher.asEquation(equation);
		newString = ""; #Gets an empty string to append to.
		for char in chars:
			#Adds each encrypted character.
			newString += Cipher.encrypt(eq,char);
		return newString; #Returns the bundled sequence as a string.

	#THe following decrypt methods practically act the same as the encrypt methods, except performing the reverse and swapping x for i.
	@staticmethod
	def decrypt(equation: str|Expr,char) -> str:
		Cipher.charCheck(char);
		eq = Cipher.asEquation(equation);
		inverse = sympy.S(sympy.solve(eq - i, x))[0];
		ordinal = ord(char);

		ordinal = inverse.subs({i: ordinal });

		if isinstance(ordinal, Integer):
			ordinal = int(ordinal);

		if not isinstance(ordinal, int):
			raise NonIntegerError(Cipher.IS_INTEGER_ERROR);
		return chr(ordinal);

	@staticmethod
	def decryptAll(equation: str|Expr,chars: str|Iterable[str]) -> str:
		eq = Cipher.asEquation(equation);
		newString = "";
		for char in chars:
			newString += Cipher.decrypt(eq,char);
		return newString;

	#Checks if encryption is possible, and returns a result if it is.
	@staticmethod
	def encryptPossible(equation: str|Expr, chars: str|Iterable[str] = allASCII) -> str:
		#Performs an encryption check on the used characters, which defaults to all ASCII characters.
		#Then, returns a constant string depending on the result.

		try:
			Cipher.encryptAll(equation,chars);
			Cipher.decryptAll(equation, Cipher.encryptAll(equation,chars));
			return Cipher.SUCCESS; #If no errors happen to this point, return a success.
		#Otherwise, of the many error cases, return a massge corresponding to that error case.
		except StringError as error:
			return Cipher.STRING_ERROR;
		except CharError as error:
			return Cipher.CHAR_ERROR;
		# except ValueError as error:
		# 	return Cipher.RANGE_ERROR;
		# except IndexError as error:
		# 	return Cipher.REVERSE_ERROR;
		# except TypeError as error:
		# 	if(str(error) == Cipher.IS_EQUATION_ERROR):
		# 		return Cipher.IS_EQUATION_ERROR;
		# 	if(str(error) == Cipher.IS_INTEGER_ERROR):
		# 		return Cipher.IS_INTEGER_ERROR;
		# 	return Cipher.VARIABLE_ERROR;
		except EquationError as error:
			return Cipher.IS_EQUATION_ERROR;
		except OverflowError as error:
			return Cipher.SIZE_ERROR;
		except NonIntegerError as error:
			return Cipher.EQUATION_CORRECT_ERROR;
		except RangeError as error:
			return Cipher.RANGE_ERROR;
		except Exception:
			return Cipher.UNKNOWN_ERROR;


	#Same as encryptPossible, except for decryption.
	@staticmethod
	def decryptPossible(equation: str|Expr, chars: str|Iterable[str] = allASCII) -> str:

		try:
			Cipher.decryptAll(equation,chars);
			Cipher.encryptAll(equation, Cipher.decryptAll(equation,chars));
			return Cipher.SUCCESS;
		except StringError as error:
			return Cipher.STRING_ERROR;
		except CharError as error:
			return Cipher.CHAR_ERROR;
		# except ValueError as error:
		# 	return Cipher.RANGE_ERROR;
		# except IndexError as error:
		# 	return Cipher.REVERSE_ERROR;
		# except TypeError as error:
		# 	if(str(error) == Cipher.IS_EQUATION_ERROR):
		# 		return Cipher.IS_EQUATION_ERROR;
		# 	if(str(error) == Cipher.IS_INTEGER_ERROR):
		# 		return Cipher.IS_INTEGER_ERROR;
		# 	return Cipher.VARIABLE_ERROR;
		except EquationError as error:
			return Cipher.IS_EQUATION_ERROR;
		except NonIntegerError as error:
			return Cipher.EQUATION_CORRECT_ERROR;
		except OverflowError as error:
			return Cipher.SIZE_ERROR;
		except RangeError as error:
			return Cipher.RANGE_ERROR;
		except Exception:
			return Cipher.UNKNOWN_ERROR;

if(__name__ == "__main__"): #Demo if the file is run directly.

	while(True):

		#For clearing the screen.
		import os;
		clear = lambda: os.system('cls' if os.name == 'nt' else 'clear'); #Multi-system terminal clear capability/

		#The string to encrypt or decrypt.
		string = input("Input a user string to cipher. Type 'cancel' to exit the program. ");

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

		#Cipher the string with the equation.
		if(typeCipher == 'c'):

			#Get the equation first.
			equation = input(f"Input an equation to use on the string, in terms of x.\nThe equation should should produce either 0 or positive values less than {0x110000}. ");
			isPossible = Cipher.encryptPossible(equation,string); #Then determines if it is possible.

			#If the equation and string cannot work together, say so and reset the loop via 'continue'.
			if(isPossible != Cipher.SUCCESS):
				clear();
				print(isPossible);
				continue;

			#Otherwise, encrypt the string and show the result.
			ciphered = Cipher.encryptAll(equation,string);

			clear();
			print('Ciphered string: ')
			print(ciphered)
			print();

			unciphered = Cipher.decryptAll(equation,ciphered);

			print('Deciphered string (reversed process): ')
			print(unciphered);

		#Otherwise, decrypt, effectively the same as encrypting but with the opposite methods.
		else:
			equation = input(f"Input the equation used to initially encrypt the string. ");
			isPossible = Cipher.decryptPossible(equation,string);
			if(isPossible != Cipher.SUCCESS):
				clear();
				print(isPossible);
				continue;

			unciphered = Cipher.decryptAll(equation,string);

			clear();
			print('Unciphered string: ')
			print(unciphered)
			print();

			ciphered = Cipher.encryptAll(equation,unciphered);

			print('Ciphered string (reversed process): ')
			print(ciphered);
