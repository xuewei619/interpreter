#-*- encoding:utf-8 -*-
'''
Created on 2016年6月8日

@author: xuewei
'''
import lex
def operate(operand_left,operator,operand_right):
    try:
        operand_left = int(operand_left)
        operand_right = int(operand_right)
    except Exception:
        operand_left = operand_left
        operand_right = operand_right
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
    
def excuteExp(node):
    if node == None:
        return node   
    
    excuteExp(node.getLeft())        
    excuteExp(node.getRight())
    if node.getLeft() != None and node.getRight() != None:        
        if not lex.isSymbol(node.getLeft().getValue()) and not lex.isSymbol(node.getRight().getValue()):
            value = operate(node.getLeft().getValue(),node.getValue(),node.getRight().getValue())
            node.setValue(value)
    return node


def execute(tree):
    if tree == None:
        return
    
    if tree.getValue() == 'if':
        executeIf(tree)
        
    if tree.getValue() == 'statement':
        executeStatement(tree)
        
    if tree.getValue() == 'ast':
        children = tree.getChildren()
        for i in range(0,len(children)):
            execute(children[i])

def executeIf(tree):
    condition = tree.getCondition()
    ifBody = tree.getIfBody()
    elseBody = tree.getElseBody()
    if excuteExp(condition).getValue():
        if ifBody:
            execute(ifBody)
    else:
        if elseBody:
            execute(elseBody)
            
def executeStatement(tree):
    expression = tree.getExpression()
    if tree.hasPrint():
        print excuteExp(expression).getValue()
