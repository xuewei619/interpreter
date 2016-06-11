#-*- encoding:utf-8 -*-
'''
Created on 2016年6月8日

@author: xuewei
'''
import lex
from ast import isKeyword

class IdentifierStack(object):
    def __init__(self):
        self.__stack = []
        
    def getStack(self):
        return self.__stack   
        
    def push(self,key,value):
        map = {"identifier" : key,"value" : value}
        if self.get(key):
            self.set(key, value)
        else:            
            self.__stack.append(map)
    
    def pop(self):
        return self.__stack.pop()
    
    def popLocal(self):
        stack = self.getStack()
        length = len(stack)
        for i in range(length - 1, -1 , -1):
            map = stack[len(stack) - 1]
            if map["identifier"] != "__local__":
                stack.pop()
            else:
                stack.pop()
                break
    
    def get(self,key):
        stack = self.getStack()
        for i in range(0,len(stack)):
            if stack[i]["identifier"] == key:
                return stack[i]["value"]
        return None
    
    def set(self,key,value):
        stack = self.getStack()
        for i in range(0,len(stack)):
            if stack[i]["identifier"] == key:
                stack[i]["value"] = value 
    
    def copy(self,obj):
        if isinstance(obj, IdentifierStack):           
            self.__stack = obj.getStack()
        else:
            raise Exception("It's not a instance of identifierStack.")
        
    def contains(self,key):
        if self.get(key):
            return True
        else:
            return False
        
def assign(token,stack):   
    try:
        token = int(token)
    except Exception:
        if token == "true":
            token = True
        elif token == "false":
            token = False
        elif not isKeyword(token):
            token = stack.get(token)
    return token


def operate(operand_left,operator,operand_right,stack):
    operand_left = assign(operand_left,stack)
    operand_right = assign(operand_right,stack)
    
    if operator == '+':
        return operand_left + operand_right
    if operator == '-':
        return operand_left - operand_right
    if operator == '*':
        return operand_left * operand_right
    if operator == '/':
        return operand_left / operand_right
    if operator == '==':
        return operand_left == operand_right
    if operator == '!=':
        return operand_left != operand_right
    if operator == '&&':
        return operand_left and operand_right
    if operator == '||':
        return operand_left or operand_right
    
def excuteExp(node,stack):
    if node == None:
        return node   
    
    excuteExp(node.getLeft(),stack)        
    excuteExp(node.getRight(),stack)
    if node.getLeft() != None and node.getRight() != None:        
        if not lex.isSymbol(node.getLeft().getValue()) and not lex.isSymbol(node.getRight().getValue()):
            value = operate(node.getLeft().getValue(),node.getValue(),node.getRight().getValue(),stack)
            node.setValue(value)
    return node


def execute(tree,stack):    
    if tree == None:
        return
    
    if stack == None:
        stack = IdentifierStack()
    
    if tree.getValue() == 'if':
        stack = executeIf(tree,stack)
        
    if tree.getValue() == 'statement':
        stack = executeStatement(tree,stack)
        
    if tree.getValue() == 'ast':
        stack.push("__local__",None)
        children = tree.getChildren()
        for i in range(0,len(children)):
            stack = execute(children[i],stack)
        stack.popLocal()
    print stack.__dict__       
    return stack

def executeIf(tree,stack):    
    condition = tree.getCondition()
    ifBody = tree.getIfBody()
    elseBody = tree.getElseBody()
    value = excuteExp(condition,stack).getValue()
    value = assign(value,stack)
    if value:
        if ifBody:
            stack = execute(ifBody,stack)
    else:
        if elseBody:
            stack = execute(elseBody,stack)
    return stack
            
def executeStatement(tree,stack):
    expression = tree.getExpression()
    if tree.hasPrint():
        value = excuteExp(expression,stack).getValue()
        value = assign(value,stack)
        print value
    
    if tree.getIdentifier() and tree.hasEqual():
        key = tree.getIdentifier()
        if expression:            
            value = excuteExp(expression,stack).getValue()
        else:
            value = None
        
        stack.push(key,value)
    return stack