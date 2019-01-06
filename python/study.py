#!/usr/bin/python
#coding:utf-8

#print "hello world"
#print "你好"
#print '%s is number %d!' %('python', 1)

#logfile = open('temp.txt', 'rw')
#print >> logfile, 'test!'
#logfile.close()
import os

# file = open('temp.txt', 'r')
# for i in file.readlines():
#     print i,
# file.close()

# file = open('temp.txt', 'a')
# while True:
# 	aline = raw_input('Enter a line, ("." to quit): ')
# 	if aline != '.':
# 	    file.write('%s%s' % (os.linesep, aline))
# 	else:
# 		break
# file.close()

def fun1(xxx):
#	print xxx
	print 'this is fun1'
	def fun2(*args, **kwargs):
		print 'this is fun2'
		print xxx(*args, **kwargs)
        print 'print fun2 end'
	return fun2

@fun1
def fun3():
	print 'this is fun3'
	return 'is me?'
    
fun3()