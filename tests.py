"""
The goal of this file is to automatically test a large array of cipher combinations from the cipher.py file to ensure no errors or unexpected results arise.
Strings are encrypted and then decrypted, and the decrypted result is compared to the original string to ensure they are both the same.
If they are not the same, an error will arise.
"""

from collections.abc import Iterable
import cipher; #Custom cipher module.
import time; #For performance measuring, use time.

#First, we will define an array of several characters, mostly English characters and punctuation but also characters such as
#the null character (the first unicode character), the last Unicode character (at 1114111), newlines, and some emojis and misc symbols.
#Then we create a bigraphic list from them - that is, every possible length-two combination of strings from this array of characters.
#Then we convert them into a tuple since tuples are immutable and the string should also be immutable.
#These strings will be the benchmark strings for the program.
testStrings = tuple(cipher.bigraphic([chr(num) for num in range(32,127)] + [chr(0), chr(1114111), "\n","🐶","🐕","🐕‍🦺","ﺚ","Ꮡ","V̿⃟⃨R̿⃟⃨U̿⃟⃨"]));
# 🐕‍🦺 = 🐕 + 🦺

def writeAccumulatedErrors():
	for string in errorReports:
		print("error - " + string);
	print("\n");
	errorReports.clear();

errorReports = [];

#-------------------------------------------------- Caesar Cipher Error test --------------------------------------------------

start = time.time();

for i in range(0,26*14):

	for string in testStrings:
		new = cipher.caesarCipher(string,i); #Encrypt
		old = cipher.caesarCipher(new,-i); #Decrypt

		if(old != string):
			errorReports.append(f"{old:>10} =/= {string:>10}  -  Caesar Cipher")

end = time.time();

print(f"Caesar Cipher test took {end - start}s to run.");
writeAccumulatedErrors()

#-------------------------------------------------- In-Place Cipher Error test --------------------------------------------------

start = time.time();

for i in range(0,26*14):

	for string in testStrings:
		new = cipher.inPlaceCaesarCipher(string,i); #Encrypt
		old = cipher.inPlaceCaesarCipher(new,-i); #Decrypt

		if(old != string):
			errorReports.append(f"{old:>10} =/= {string:>10}  -  In-Place Cipher")

end = time.time();

print(f"In-Place Cipher test took {end - start}s to run.");
writeAccumulatedErrors();

#-------------------------------------------------- Code Point Cipher Error test --------------------------------------------------

start = time.time();

for i in range(0,26*14):

	for string in testStrings:

		stringRange = cipher.codePointRange(string);

		new = cipher.codePointCaesarCipher(string,i); #Encrypt
		old = cipher.codePointCaesarCipher(new,-i, stringRange[0], stringRange[1]); #Decrypt

		if(old != string):
			errorReports.append(f"{old:>10} =/= {string:>10}  -  Code Point Cipher")

end = time.time();

print(f"Code Point Cipher test took {end - start}s to run.");
writeAccumulatedErrors()

#-------------------------------------------------- Symbol Map Cipher Error test --------------------------------------------------

start = time.time();

times = 0;

for maps in [
	("full-set","񠦓𚱴񡐶𐗙𘲢򊘱񳏭򎙤𮅃𯐳𢽫񉖑򏜻𸲺𙰨񨽸񁹎񐽚񓌙򕱧񫥭񕱰郌񐤁񂋃񮫹𶭣򙮤🷩񍖡𼼅𽁄񎯐𮼻񁏆񹦕񋩤񫿓򒔗񒮾񔐊񿒈񜲝񦡉򊗢񎓞񪁍𒷱𞋄𵾹𴣰𷡮񋷙𖌓񧀨𷠴𥽅񟍭אּ񍧏񽜢𐀱񮶕򗰍񊛜񛠞񘧱򒳇򃋼𤃈𠈌񥫥񗂰𠬩𽡮񭽊𚦺𢕏񧖄𲗏𨕓𗯌񕝻񏊡򓺣񿿷񼞖񶄩񓴱򖰀񯝈򀬛򀀶򘮕񎷼"),
	("alpha-numeric","񸨒񁪣򖻼򐠨𯫔𔲓𫆧𪨆񜐌򂉎񅲫񷔗𵗶𺏑𖈈򃤘񆦅򁜮抱잇񰮀񾚘򑤚𵓒򇂘𚜍񮱽򆗆񥅱𗆇񏪊𴪺𺖍򖼼錸񜎼񪬵񪺯򎼮𗎂𢵍񬃇𩜠񉝧򗙜񂛳򌓾񓴪񴳁񂬗񏟃򎠨񩍄򈮋𦳚񊂳񣌚񽻯솱𒴔񬭜𳱽"),
	("".join(cipher.lowered(cipher.alphabet)),"򘏭뮜򋋧򔠄𾛩𶶡񈗑񎫿𧜙񕂂񙺵먴񚵈񝽦𑘌𖑐쉛񏧷򁟋򑆧񘗳𳤭𫢱񗞔񙡰"),

	("bigraphic:full-set","".join([chr(num) for num in range(9000,9000+96**2)])),
]:

	for string in testStrings:

		times += 1;

		print(f"{maps[0]} - {times} / {len(testStrings) * 4}                          ",end="\r");

		new = cipher.symbolMapCipher(maps[0],maps[1],string); #Encrypt
		old = cipher.symbolMapCipher(maps[1],maps[0],new); #Decrypt

		if(old != string):
			errorReports.append(f"{"'"+old+"'":>12} =/= {"'"+string+"'":>12}  -  Symbol Map Cipher")

end = time.time();

print(f"Symbol Map Cipher test took {end - start}s to run.");
writeAccumulatedErrors()

#-------------------------------------------------- Algebraic Cipher Error test --------------------------------------------------

start = time.time();

for eq in ["x+10", "x*2", "x*3 + 90"]:

	for string in testStrings:
		result = cipher.AlgebraicCipher.encryptPossible(eq,string);
		#The "encryptpossible" function checks if a string can be encrypted AND decrypted with the given equation.
		#It returns a string based on the result.

		if(result != cipher.AlgebraicCipher.SUCCESS and result != cipher.AlgebraicCipher.SIZE_ERROR and result != cipher.AlgebraicCipher.RANGE_ERROR):
			#If the result fails, but not because of a size error or range error, show the equation and the string it failed to cipher and the error message.
			print(f"{eq:>6} | {string:>10} | {result}")

end = time.time();

print(f"Algebraic Cipher took {end - start}s to run.");
writeAccumulatedErrors()
