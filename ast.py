#-*- encoding:utf-8 -*-
'''
Created on 2016年5月27日

@author: xuewei
'''
import exp
class ast(object):
    def __init__(self,value):
        self.__value = value
        self.__children = []
        
    def appendChild(self,obj):
        self.__children.append(obj)
        
    def setEndIndex(self,index):
        self.__endIndex = index
     
    def getEndIndex(self):
         return self.__endIndex
        
    
class FunctionStatement(ast):
    def __init__(self,name):
        self.__value = name
        
    def appendBody(self,body):
        self.appendChild(body)
        
        
class IfStatement(ast):
    def __init__(self):
        super(IfStatement,self).__init__('if')
        
    def appendCondition(self,condition):
        self.appendChild(condition)
        
    def appendifBody(self,ifBody):
        self.appendChild(ifBody)
        
    def appendelseBody(self,elseBody):
        self.appendChild(elseBody)
        
    def setEndIndex(self,index):
        self.__endIndex = index
     
    def getEndIndex(self):
         return self.__endIndex
        
class WhileStatement(ast):
    def __init__(self):
        self.__value = "while"
        
    def appendCondition(self,condition):
        self.appendChild(condition)
        
    def appendBody(self,body):
        self.appendBody(body)
        
#找到下一个括号 list[index]必须是(
def findNextBracket(list,index):
    stack = []
    list_length = len(list)
    for i in range(index, list_length):
        if list[i] == '(' or list[i] == ')':        
            length = len(stack)  
            if length > 0:
                if stack[length - 1] != list[i]:
                    stack.pop()
                else:
                    stack.append(list[i])
            else:
                stack.append(list[i])
        if len(stack) == 0:
            return i

#找到下一个大括号 list[index]必须是{   
def findNextBrace(list,index):
    stack = []
    list_length = len(list)
    for i in range(index, list_length):
        if list[i] == '{' or list[i] == '}':        
            length = len(stack)  
            if length > 0:
                if stack[length - 1] != list[i]:
                    stack.pop()
                else:
                    stack.append(list[i])
            else:
                stack.append(list[i])
        if len(stack) == 0:
            return i
        
def parseList(list,index):
    tree = ast('ast')
    length = len(list)
    while index < length:
        if list[index] == 'if':            
            ifStmt = parseIf(list,index)
            tree.appendChild(ifStmt)
            index = ifStmt.getEndIndex()
            continue
            
        index += 1
    tree.setEndIndex(index)
    return tree
    

def parseIf(list,index):     
    
    ifStmt = IfStatement()
    length = len(list)    
    while index < length:
        if list[index] == '(':
            offset = findNextBracket(list, index)
            exp_list = list[index+1:offset]
            condition = exp.generateTree(exp_list)
            ifStmt.appendCondition(condition)
            index = offset + 1            
        
        if index < length and list[index] == '{':
            offset = findNextBrace(list, index)
            ifbody_list = list[index+1:offset]
            ifBody = parseList(ifbody_list, 0)
            ifStmt.appendifBody(ifBody)
            index = offset + 1
        
        if index < length and list[index] == 'else':
            index += 1
            offset = findNextBrace(list, index)
            elsebody_list = list[index+1:offset]
            elseBody = parseList(elsebody_list, 0)
            ifStmt.appendelseBody(elseBody)
            index = offset + 1            
        index += 1
    ifStmt.setEndIndex(index)
    return ifStmt
        
