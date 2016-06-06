#-*- encoding:utf-8 -*-
'''
Created on 2016年5月23日

@author: xuewei
'''
import lex,exp,ast
string = "if(1==2){if(1=1){aaa}}else{aaaa}"
list = lex.split(string)
print list
tree = ast.parseList(list,0)
print tree

