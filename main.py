#-*- encoding:utf-8 -*-
'''
Created on 2016年5月23日

@author: xuewei
'''
import lex,ast
string = "if(1==2){function(a,b,c){var a = 1;var b = a;}}else{var a = 2; var b = a;}"
list = lex.split(string)
print list
tree = ast.parseList(list,0)
print tree

