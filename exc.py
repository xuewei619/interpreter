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