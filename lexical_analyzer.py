import re  											#This module is for using regex expressions.
import sys											#this module is used for system calls.

delim="\t","\n",",",";","(",")","{","}","[","]","<",">",">=","<=","==","!="," ","=","+","-","*","/"  #this is list of delimiters.

opera=['+','-','*','/']     #this is list of arithmetic operators.
operb=['and','or','not']     #this is list of boolean operators.
operr=['>','<','>=','<=','==','!=']  #this is list of relational operators.
key=["void","if","else","return","skip","while","do"]  #this is list of keywords.
type=["int","char"]                        #this is list of valid data types.
symbol_table={}                #this is symbol table



def main():
	a=""
	a=input("Enter the file name:")	                #take input file name ex. "test.txt"
	txt=open(a)                                     #open file
	str1=txt.read()
	sentencelist=str1.split(';')                    #split content of file wrt ';'
	sentencelist=remove(sentencelist)               #remove(x) removes '' (empty elements) from x.
	arr=[]
	
	add_operators(a,symbol_table)                  #adds operators to symbol_table
	for sentence in sentencelist:
		arr=re.split("[\s\t\n]+",sentence)     #split each sentence wrt spaces,tab,new line and stores in arr.
		arr=remove(arr)                        #removes empty elememts from arr.
		if(belongs(arr[0],type)):              #if senetnce is declaring some variable,send the arr into declaration()
			declaration(arr,symbol_table)  
		else:                                  #else, in all other cases ex. a=b+c or if(a<b) arr is sent into other()
			other(arr,symbol_table)
	print_table(symbol_table)                     #finally  printing symbol table


def belongs(str,arr):                                 #returns true if str is present in arr[]
	for i in arr:
		if(str==i):
			return True
	return False

def declaration(arr,symbol_table):                    #handles variable declaration statements
	if(len(arr)==1):
		print "error in this sentence:"+arr   #if statement has only 'int' or 'char' ex. int; -> gives error
		sys.exit("error occurred")
	arr2=[]
	for i in range(1,len(arr)):                  
		arr2=re.split("[,=+-/*%]",arr[i])    #splits statement using delimiters ,=+-/*% and stores in arr2
		arr2=remove(arr2)                    #removes any empty elements from arr2
		for token in arr2:                   #iterating over arr2
			if(is_identifier(token)):    #checks if token is identifier according to C convention
				check_and_add(token,arr[0],symbol_table)  #checks if identifier already declared,else adds to symbol_table
			else:                        #if tokendoes not follow identifier's rules
				print token+" is not an identifier!"
				print "exiting..."
				sys.exit()


def remove(arr):                                     #removes any empty elements('') from arr.
	while (belongs('',arr)):		
		arr.remove('')
	return arr


def is_identifier(token):                       #checks if token is following rules for identifier using regex : [a-zA-Z_]([a-zA-Z0-9_])*
	if(re.match("[0-9]+",token)):
		return True
	elif belongs(token,key):
		return True
	else:
		return re.match("[a-zA-Z_]([a-zA-Z0-9_])*",token)
       
def check_and_add(token,value,symbol_table):         #checks if identifier already declared,else adds to symbol_table
	if(token.isdigit()):                             #checks if token is only a number.
		pass;
	elif token not in symbol_table:
		symbol_table[token]=value            #adding token to symbol table after checking.
	else:
		print token+" is already declared!"
		print "exiting..."
		sys.exit()

		
def check(token,symbol_table):                 #checks if identifier is keyword or if its already present in symbol_table else, gives error.
	if(token.isdigit()):
		pass;
	elif (belongs(token,key)):
		symbol_table[token]="keyword"          #adding keyword to symbol_table
	elif token not in symbol_table:
		print token+" not declared!"
		print "exiting..."
		sys.exit()

def other(arr,symbol_table):                            #handles all statements except declaration statements
	for i in range(len(arr)):
		regexPattern = '|'.join(map(re.escape, delim))  #generating regex for splitting each element in arr.
		arr2=re.split(regexPattern,arr[i])
		arr2=remove(arr2)                    #remove empty elements from arr2
		for token in arr2:
			if(is_identifier(token)):        #checks if token is identifier
				check(token,symbol_table)    #checks if token is keyword or if its already present in symbol_table else, gives error.
			else:
				print token
				print "%s is not an other identifier!"%token
				print "exiting..."
				sys.exit()

def add_operators(a,symbol_table):
	txt=open(a)                                  #open file
	str1=txt.read()
	operatorlist=re.split("[a-zA-Z0-9]+",str1)      #split wrt regex [a-zA-Z]
	print operatorlist
	for token in operatorlist:
		if(belongs(token,opera) or belongs(token,operb) or belongs(token,operr)):
			symbol_table[token]="operator"


def print_table(symbol_table):                        #prints symbol table in required format.
	i=1
	size="sfvdfn"
	print "token    type      size"
	for key in symbol_table:
		if(symbol_table[key]=="int"):
			size="8"
		if(symbol_table[key]=="char"):
			size="2"
		if(symbol_table[key]=="keyword" or symbol_table[key]=="operator"):
			size="Null"
		print key+"     "+symbol_table[key]+"    "+size
main()				



