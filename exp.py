#-*- encoding:utf-8 -*-
'''
Created on 2016年5月27日

@author: xuewei
'''
from compiler.ast import Node
symbols = ['+','-','*','/','(',')','==','!=','||','&&']
priority = {"+":1,"-":1,"*":2,"/":2,"(":0,")":0,'==':3,'!=':3,'||':3,'&&':3}

class exp(object):
	def __init__(self,value):
		self.__value = value
		self.__left = None
		self.__right = None
		
	def getValue(self):
		return self.__value
	
	def setValue(self,value):
		self.__value = value

	def setLeft(self,obj):
		self.__left = obj

	def getLeft(self):
		return self.__left

	def setRight(self,obj):
		self.__right = obj

	def getRight(self):
		return self.__right

#string = "1+2*3+2+4*3"
string = "1+2*3+1-2*3"
#判断是否是运算符号
def isSymbol(char):
	length = len(symbols)
	for i in range(0,length):
		if char == symbols[i]:
			return True
	return False

#过滤括号
def noBrackets(char):
	if char == ')' or char == '(':
		return False
	return True
	
#判断是否是逻辑运算符
def isLogicOperator(string,i):
	length = len(string)
	if string[i] == '=':
		if i < length - 1 and string[i + 1] == '=':
			return True
		
	if string[i] == '!':
		if i < length - 1 and string[i + 1] == '=':
			return True
		
	if string[i] == '|':
		if i < length - 1 and string[i + 1] == '|':
			return True
	
	if string[i] == '&':
		if i < length - 1 and string[i + 1] == '&':
			return True
	return False

#先分词
def split(string):
	i = 0
	length = len(string)
	list = []
	while i < length:		
		if isLogicOperator(string, i):
			list.append(string[i] + string[i + 1])
			i += 2
			continue						
		
		if isSymbol(string[i]):			
			list.append(string[i])
			i += 1
			continue	

		j = i
		number = ''		
		while j < length and not isSymbol(string[j]) and not isLogicOperator(string, j):			
			if not string[j] == ' ':
				number += string[j]
			j += 1				
		list.append(number)		
		i = j 
		
	return list

#逆波兰式
def rpn(list):	
	operators = []
	numbers = []
	rpn_list = []
	length = len(list)
	
	for i in range(0,length):			
		current = list[i]
		if not isSymbol(current):
			numbers.append(current)
		else:
			operators_length = len(operators)
			for j in range(0,operators_length):
				if priority[current] <= priority[operators[len(operators) - 1]] and not current == "(":
					rpn_list.extend(numbers)
					rpn_list.append(operators.pop())					
					numbers = []
				else:
					break
			operators.append(current)
			
	rpn_list.extend(numbers)
	operators.reverse()
	rpn_list.extend(operators)
	return filter(noBrackets,rpn_list)

def addNode(head,value):
	if not head:
		return head
	child = exp(value)
	if not head.getLeft():
		head.set
		
					
def tree(list,index):
	length = len(list)
	node = None			
	if not isSymbol(list[index]):
		return exp(list[index])
	
	node = exp(list[index])
	if index > 1 and isSymbol(list[index - 1]) and not isSymbol(list[index - 2]):
		node.setRight(tree(list,index - 1))
 		node.setLeft(tree(list,findNext(list,index)))
 	else:
 		node.setRight(tree(list,index - 1))
 		node.setLeft(tree(list,index - 2))				
	return node

def findNext(list,index):
	for i in range(index-2,-1,-1):
		if isSymbol(list[i]):
			return i
	return index - 4
		

def preview(tree):
	if tree == None:
		return
	print tree.getValue()
	preview(tree.getLeft())
	#print tree.getValue()
	preview(tree.getRight())
	
	
list = split(string)

rpn_list = rpn(list)
print rpn_list
_tree = tree(rpn_list,len(rpn_list) -1)
preview(_tree)