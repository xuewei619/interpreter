#-*- encoding:utf-8 -*-
'''
Created on 2016年5月27日

@author: xuewei
'''
import exp,lex
keywords = ['var','function','if','while','print','return','true','false']
class ast(object):
    def __init__(self,value):
        self.__value = value
        self.__children = []
        
    def appendChild(self,obj):
        self.__children.append(obj)    
        
    def getValue(self):
        return self.__value 
    
    def getChildren(self):
        return self.__children
        
class Statement(ast):
    def __init__(self):
        super(Statement,self).__init__('statement')
        self.__identifier = None
        self.__hasEqual = False
        self.__hasPrint = False
        self.__hasReturn = False
        self.__hasVar = False
    
    def getValue(self):
        return super(Statement,self).getValue()
    
    def getChildren(self):
        return super(Statement,self).getChildren()
    
    def setIdentifier(self,name):
        self.__identifier = name
        
    def getIdentifier(self):        
        return self.__identifier    
    
    def setExpression(self,exp):
        self.__exp = exp
        
    def getExpression(self):
        return self.__exp    
    
    def setHasVar(self,bool):
        self.__hasVar = bool
    
    def hasVar(self):
        return self.__hasVar
    
    def setHasEqual(self,bool):
        self.__hasEqual = bool
    
    def hasEqual(self):
        return self.__hasEqual    
    
    def setHasReturn(self,bool):
        self.__hasReturn = bool
    
    def hasReturn(self):
        return self.__hasReturn
    
    def setHasPrint(self,bool):
        self.__hasPrint = bool
    
    def hasPrint(self):
        return self.__hasPrint
    
    
class FunctionStatement(ast):
    def __init__(self):
        super(FunctionStatement,self).__init__('function')
        self.__arguments = []
        
    def getValue(self):
        return super(FunctionStatement,self).getValue()
    
    def getChildren(self):
        return super(FunctionStatement,self).getChildren()
    
    def setName(self,name):
        self.__name = name
    
    def getName(self):
        return self.__name
    
    def appendArguments(self,param):
        self.__arguments.append(param)    
        
    def appendBody(self,body):
        self.appendChild(body) 
        
    def getArguments(self):
        return self.__arguments
        
        
class IfStatement(ast):
    def __init__(self):
        super(IfStatement,self).__init__('if')
        
    def getValue(self):
        return super(IfStatement,self).getValue()
    
    def getChildren(self):
        return super(IfStatement,self).getChildren()
        
    def appendCondition(self,condition):
        self.appendChild(condition)
        
    def appendIfBody(self,ifBody):
        self.appendChild(ifBody)
        
    def appendElseBody(self,elseBody):
        self.appendChild(elseBody)
        
    def getCondition(self):
        children = self.getChildren()
        if children[0]:
            return children[0]
        return None
    
    def getIfBody(self):
        children = self.getChildren()
        if children[1]:
            return children[1]
        return None
    
    def getElseBody(self):
        children = self.getChildren()
        if children[2]:
            return children[2]
        return None
    
        
class WhileStatement(ast):
    def __init__(self):
        super(WhileStatement,self).__init__('while')
        
    def getValue(self):
        return super(WhileStatement,self).getValue()
    
    def getChildren(self):
        return super(WhileStatement,self).getChildren()
        
    def appendCondition(self,condition):
        self.appendChild(condition)
        
    def appendBody(self,body):
        self.appendChild(body)
    
    def getCondition(self):
        children = self.getChildren()
        if children[0]:
            return children[0]
        return None
    
    def getBody(self):
        children = self.getChildren()
        if children[1]:
            return children[1]
        return None
        
#找到结束括号
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
    return None

#找到结束大括号
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
    return None

#找封号
def findSemicolon(list,index):
    length = len(list)
    for i in range(index,length):
        if list[i] == ';':
            return i
    return None

def getCondition(list,index):
    offset = findEndBracket(list, index)
    exp_list = list[index+1:offset]
    condition = exp.generateTree(exp_list)
    return {"condition" : condition,"offset" : offset}

def getBody(list,index):
    offset = findEndBrace(list, index)
    body_list = list[index + 1 : offset]
    result = parseList(body_list, 0)
    body = result["statement"]
    return {"body" : body,"offset" : offset}

def isKeyword(word):
    flag = False
    for i in range(0,len(keywords)):
        if word == keywords[i]:
            flag = True
            break
    return flag
        
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
        
        if list[index] == 'function':
            result = parseFunc(list, index)
            tree.appendChild(result["statement"])
            index = result["offset"]
            continue
        
        result = parseStmt(list, index)
        tree.appendChild(result["statement"])
        index = result["offset"]            
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
            continue       
        
        if index < length and list[index] == '{':
            result = getBody(list, index)
            ifBody = result["body"]
            offset = result["offset"]
            ifStmt.appendIfBody(ifBody)
            index = offset + 1
            continue
        
        if index < length and list[index] == 'else':
            index += 1
            result = getBody(list, index)
            elseBody = result["body"]
            offset = result["offset"]
            ifStmt.appendElseBody(elseBody)
            index = offset + 1    
            break        
        
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
            continue
            
        if list[index] == '{':
            result = getBody(list, index)
            whileBody = result["body"]
            offset = result["offset"]
            whileStmt.appendCondition(whileBody)
            index = offset + 1
            break
        
        index += 1
    return {"statement" : whileStmt,"offset" : index}

def parseFunc(list,index):
    functionStmt = FunctionStatement()
    length = len(list)
    while index < length:        
        if list[index] == 'function':
            index += 1
            functionStmt.setName(list[index])
            continue
        
        if list[index] == '(':
            offset = findEndBracket(list, index)
            params = list[index + 1 : offset]
            for i in range(0,len(params)):
                if not lex.isSymbol(params[i]):
                    functionStmt.appendArguments(params[i])    
            index = offset + 1
            continue
        
        if list[index] == '{':
            result = getBody(list, index)
            funcBody = result["body"]
            offset = result["offset"]
            functionStmt.appendBody(funcBody)
            index = offset + 1
            break
        
        index += 1
    return {"statement" : functionStmt,"offset":index}

def parseStmt(list,index):
    stmt = Statement()
    length = len(list)
    offset = findSemicolon(list, index)
    while index < offset:        
        if list[index] == 'var':
            stmt.setHasVar(True)
            index += 1
            continue       
        
        if  list[index] == '=':           
            exp_list = list[index + 1 : offset]
            exp_tree = exp.generateTree(exp_list)
            stmt.setExpression(exp_tree)
            stmt.setHasEqual(True)
            break
        
        if list[index] == 'return':
            offset = findSemicolon(list, index)
            exp_list = list[index + 1 : offset]
            exp_tree = exp.generateTree(exp_list)
            stmt.setExpression(exp_tree)
            stmt.setHasReturn(True)
            break
        
        if list[index] == 'print':
            offset = findSemicolon(list, index)
            exp_list = list[index + 1 : offset]
            exp_tree = exp.generateTree(exp_list)
            stmt.setExpression(exp_tree)
            stmt.setHasPrint(True)
            break
        
        #####identifier
        if not isKeyword(list[index]):
            stmt.setIdentifier(list[index])
            index += 1
            continue
     
        index += 1
    return {"statement" : stmt,"offset" : offset + 1}         
