#-*- encoding:utf-8 -*-
'''
Created on 2016年5月23日

@author: xuewei
'''
import lex,exp,ast,exc
from exc import IdentifierStack
from ast import  isKeyword

# string = "(4*5) + (2*3)"
# list = lex.split(string)
# print list
# tree = exp.generateTree(list)
# print exc.excuteExp(tree).getValue()


string = "var a=0;while(a < 100){print a;a = a + 1;} print a;"
list = lex.split(string)
print list
tree = ast.parseList(list,0)
print tree

exc.execute(tree["statement"],None)
# map = IdentifierStack()
# map.push("local",2)
# print map.__dict__
# map.push("local",1)
# print map.__dict__

