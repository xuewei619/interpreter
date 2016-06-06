#-*- encoding:utf-8 -*-
'''
Created on 2016年5月27日

@author: xuewei
'''
import lex

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

#过滤括号
def noBrackets(char):
	if char == ')' or char == '(':
		return False
	return True

#逆波兰式
def rpn(list):	
	operators = []
	numbers = []
	rpn_list = []
	length = len(list)
	
	for i in range(0,length):			
		current = list[i]
		if not lex.isSymbol(current):
			numbers.append(current)
		else:
			operators_length = len(operators)
			for j in range(0,operators_length):
				if priority[current] <= priority[operators[len(operators) - 1]] and current != "(":
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
	
#生成二叉树
def tree(list,index):
	length = len(list)
	node = None			
	if not lex.isSymbol(list[index]):
		return exp(list[index])
	
	node = exp(list[index])
	if index > 1 and lex.isSymbol(list[index - 1]) and not lex.isSymbol(list[index - 2]):
		node.setRight(tree(list,index - 1))
 		node.setLeft(tree(list,findNext(list,index)))
 	else:
 		node.setRight(tree(list,index - 1))
 		node.setLeft(tree(list,index - 2))				
	return node

def generateTree(list):
	list = rpn(list)
	return tree(list,len(list) - 1)

def findNext(list,index):
	for i in range(index-2,-1,-1):
		if lex.isSymbol(list[i]):
			return i
	return index - 4
		

def preview(tree):
	if tree == None:
		return
	print tree.getValue()
	preview(tree.getLeft())
	#print tree.getValue()
	preview(tree.getRight())

