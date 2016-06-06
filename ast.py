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
    
class FunctionStatement(ast):
    def __init__(self,name):
        super(FunctionStatement,self).__init__('function')
        self.__arguments = []
    
    def appendArguments(self,param):
        self.__arguments.append(param)    
        
    def appendBody(self,body):
        self.appendChild(body) 
        
    def getArguments(self):
        return self.__arguments
        
        
class IfStatement(ast):
    def __init__(self):
        super(IfStatement,self).__init__('if')
        
    def appendCondition(self,condition):
        self.appendChild(condition)
        
    def appendifBody(self,ifBody):
        self.appendChild(ifBody)
        
    def appendelseBody(self,elseBody):
        self.appendChild(elseBody)
    
        
class WhileStatement(ast):
    def __init__(self):
        super(WhileStatement,self).__init__('while')
        
    def appendCondition(self,condition):
        self.appendChild(condition)
        
    def appendBody(self,body):
        self.appendChild(body)
        
#找到结束括号 list[index]必须是(
def findEndBracket(list,index):
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

#找到结束大括号 list[index]必须是{   
def findEndBrace(list,index):
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

def getCondition(list,index):
    offset = findEndBracket(list, index)
    exp_list = list[index+1:offset]
    condition = exp.generateTree(exp_list)
    return {"condition" : condition,"offset" : offset}

def getBody(list,index):
    offset = findEndBrace(list, index)
    body_list = list[index+1:offset]
    result = parseList(body_list, 0)
    body = result["statement"]
    return {"body" : body,"offset" : offset}
    
        
def parseList(list,index):
    tree = ast('ast')
    length = len(list)
    while index < length:
        if list[index] == 'if':            
            result = parseIf(list,index)
            tree.appendChild(result["statement"])
            index = result["offset"]
            continue
        
        if list[index] == 'while':            
            result = parseWhile(list,index)
            tree.appendChild(result["statement"])
            index = result["offset"]
            continue
            
        index += 1
    
    return {"statement" : tree,"offset" : index}
    

def parseIf(list,index):     
    
    ifStmt = IfStatement()
    length = len(list)    
    while index < length:
        if list[index] == '(':            
            result = getCondition(list, index)
            condition = result["condition"]
            offset = result["offset"]
            ifStmt.appendCondition(condition)
            index = offset + 1            
        
        if index < length and list[index] == '{':
            result = getBody(list, index)
            ifBody = result["body"]
            offset = result["offset"]
            ifStmt.appendifBody(ifBody)
            index = offset + 1
        
        if index < length and list[index] == 'else':
            index += 1
            result = getBody(list, index)
            elseBody = result["body"]
            offset = result["offset"]
            ifStmt.appendelseBody(elseBody)
            index = offset + 1            
        index += 1
    return {"statement" : ifStmt, "offset": index}


def parseWhile(list,index):
    
    whileStmt = WhileStatement()
    length = len(list)
    while index < length:
        if list[index] == '(':
            result = getCondition(list, index)
            condition = result["condition"]
            offset = result["offset"]
            whileStmt.appendCondition(condition)
            index = offset + 1
            
        if list[index] == '{':
            result = getBody(list, index)
            whileBody = result["body"]
            offset = result["offset"]
            whileStmt.appendCondition(whileBody)
            index = offset + 1
        
        index += 1
    return {"statement" : whileStmt,"offset" : index}

# def parseFunc(list,index):
#     functionStmt = FunctionStatement()
#     length = len(list)
#     while index < length:
#         if list[index] == '(':
#             index += 1
#         if list[index] == '{':
#             result = getBody(list, index)
#             funcBody = result["body"]
#             offset = result["offset"]
#             functionStmt.appendBody(body)
            