#-*- encoding:utf-8 -*-
'''
Created on 2016年5月23日

@author: xuewei
'''

global keywords
global stack
keywords = ['var','func','loop','while']
#status : 正常读取 0 注释 1
stack = []

'''
    普通变量
'''
class varialble:   
    def __findId(self,name):
        length = len(keywords)
        isFind = False
        for i in range(0,length):
            if keywords[i] == name:
                self.__id = i
                isFind = True
                break
        if not isFind:
            self.__id = -1   
                
    
    def __init__(self,name,line):
        self.__name = name
        self.__line = line
        self.__findId(name)
    
    def getName(self):
        return self.__name
    
    def setName(self,name):
        self.__name = name
    
    def getLine(self):
        return self.__line
    
    def setLine(self,line):
        self.__line = line
        
    def getId(self):
        return self.__id
    
    def setId(self,id):
        self.__id = id
    
    def getValue(self):
        return self.__value
    
    def setValue(self,value):
        self.__value = value

'''
    方法类
'''

def isCharacter(char):    
    return (ord(char) >= ord('a') and ord(char) <= ord('z')) or (ord(char) >= ord('A') and ord(char) <= ord('Z'))

def isNumber(char):
    return ord(char) >= ord('0') and ord(char) <= ord('9')

def isCharacterOrNumber(char):
    return isCharacter(char) or isNumber(char)

def isExpVariable(exp):
    flag = True
    if not isCharacter(exp[0]):
        return False
    for i in range(1,len(exp)):
        if not isCharacterOrNumber(exp[i]):
            flag = False
    return flag

def getValueByName(name):
    for i in range(0,len(stack)):
        if stack[i].getName() == name:
            return stack[i].getValue()
    return None

def parse(script):
    global status
    status = 0
    line = 1
    length = len(script)
    i = 0
    while i < length:
        #print script[i]
        if script[i] == '\n':
            line += 1
        
        #跳过空格
        if script[i] == ' ' or status == 1:
            i += 1
            continue
        
        #解析等号后的表达式
        if script[i] == '=':
            j = i + 1
            expression = ''
            while not script[j] == ',' and not script[j] == ';':
                if not script[j] == ' ':
                    expression += script[j]
                j += 1
            #如果是变量
            if isExpVariable(expression):
                pre_variable = stack.pop()
                value = getValueByName(expression)
                pre_variable.setValue(value)
                stack.append(pre_variable)
            else:
                v = stack.pop()            
                v.setValue(eval(expression))
                stack.append(v)
            i = j
            continue
        
        
        #解析字母
        if isCharacter(script[i]):
            j = i
            name = ''
            while isCharacterOrNumber(script[j]):
                name += script[j]
                j += 1
            i = j 
            
            if name == 'log':
                output = ''               
                while not  script[j] == ';':
                    if not script[j] == ' ':
                        output += script[j]
                    j += 1
                output = getValueByName(output)                
                i = j
                if output:
                    print output
                else:
                    print "null"
                continue
            #先判断这个变量是否入栈
            index = -1
            for o in range(0,len(stack)):
                if stack[o].getName() == name:
                    index = o
                    break
            
            #如果不在栈中，就新建一个变量压入栈中
            if index == -1:
                new_variable = varialble(name,line)
                stack.append(new_variable)
            #如果在栈中，就把它放到栈顶
            else:
                existed_variable = stack.pop(index)
                stack.append(existed_variable)           
            continue
            
            
        i += 1
#         if script[i] == '/':
#             if i < length:
#                 if script[i + 1] == '*':
#                     status = 1
#                     continue
#             if i > 0:
#                 if script[i - 1] == '*':
#                     status = 0
#                 
#         print script[i]
       
str = "a = 12,b = a;log b;"

parse(str)
for i in range(0,len(stack)):
    print stack[i].getName()