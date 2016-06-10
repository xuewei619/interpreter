#-*- encoding:utf-8 -*-
'''
Created on 2016年5月23日

@author: xuewei
'''
import lex,exp,ast,exc

# string = "(4*5) + (2*3)"
# list = lex.split(string)
# print list
# tree = exp.generateTree(list)
# print exc.excuteExp(tree).getValue()


string = "if(1==1){print 1*2+3;}else{print 2;}"
list = lex.split(string)
print list
tree = ast.parseList(list,0)
print tree

exc.execute(tree["statement"])
                

