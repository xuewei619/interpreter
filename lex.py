#-*- encoding:utf-8 -*-
'''
Created on 2016年6月1日

@author: xuewei
'''

symbols = ['+','-','*','/','(',')',',','=',';','{','}','[',']']
#判断是否是运算符号
def isSymbol(char):
    length = len(symbols)
    for i in range(0,length):
        if char == symbols[i]:
            return True
    return False

def isCharacter(char):
    if (ord(char) >= ord('A') and ord(char) <= ord('Z')) or (ord(char) >= ord('a') and ord(char) <= ord('z')):
        return True
    return False

def isNumber(char):
    if ord(char) >= ord('0') and ord(char) <= ord('9'):
        return True
    return False

def findCommentsEnd(string,start):
    length = len(string)
    end = start
    while end < length:
        if end > 0  and string[end] == '/' and string[end - 1] == '*':
            return end
        end += 1
    return length - 1

def split(string):
    length = len(string)
    list = []
    index = 0
    while index < length:
        
        #跳过注释
        if index < length - 1 and string[index] == '/' and string[index + 1] == '*':
            offset = findCommentsEnd(string, index)
            index += offset + 1
            continue
        
        #关键字或变量或方法名       
        if isCharacter(string[index]):
            token = string[index]
            offset = index + 1
            while offset < length and not isSymbol(string[offset]) and string[offset] != ' ':
                token += string[offset]
                offset += 1
            list.append(token)
            index = offset
            continue
        
        #整数和浮点数
        if isNumber(string[index]):
            token = string[index]
            offset = index + 1
            while offset < length and (isNumber(string[offset]) or string[offset] == '.'):
                token += string[offset]
                offset += 1
            list.append(token)
            index = offset
            continue
        
        #各种符号
        if isSymbol(string[index]):
            list.append(string[index])
        
        index += 1
    return list
          