#-*- encoding:utf-8 -*-
'''
Created on 2016年5月27日

@author: xuewei
'''

class ast(object):
    def __init__(self,value):
        self.__value = value
        self.__children = []
        
    def appendChild(self,obj):
        self.__children.append(obj)
        
    
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
        
class WhileStatement(ast):
    def __init__(self):
        self.__value = "while"
        
    def appendCondition(self,condition):
        self.appendChild(condition)
        
    def appendBody(self,body):
        self.appendBody(body)
        
        

def findPreBrace(string,index):
    
    length = len(string)
    while not script[index] == '{':
        if not index == length - 1:
            print "error: no prebraces"
            return None
        index += 1
    return index

def parseIf(string,parent,index):
    ifStmt = IfStatement()    
    #condition
    begin = index
    index = findPreBrace(string, begin)            
    condition = string[begin:index]
    index += 1
    print condition
    ifStmt.appendCondition(condition)
    #if_body
    index += 1
    ifBody = ''
    while not string[index] == '}':
        if not string[index] == ' ':
            ifBody += string[index]
        index += 1
    print ifBody
    ifStmt.appendifBody(ifBody)
    #else_body
    index += 1
    while True:
        if string[index] == ' ':
            index += 1
            continue                
        if string[index] == 'e':
            if index < length - 3 and string[index:index+4] == 'else':
                index += 3
                index = findPreBrace(string, index)
                index += 1
                elseBody = ''
                while not string[index] == '}':
                    if not string[index] == ' ':
                        elseBody += string[index]
                    index += 1 
                print elseBody
                ifStmt.appendelseBody(elseBody)
        else:
            break


script = "if(1==1)"
tree = ast("content")
i = 0
length = len(script)
while(i < length):
    if script[i] == "i":
        if i < length - 1 and script[i + 1] == "f":
            i += 2
            parseIf(script, tree, i)
             
                
    i+=1

