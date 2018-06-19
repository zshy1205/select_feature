# -*- coding: utf-8 -*-

import codecs
import os
import sys
import io

def cut(SourseFile, ChineseFile, EnglishFile):
	CHINESE = io.open(ChineseFile, 'w', encoding='utf-8')
	ENGLISH = io.open(EnglishFile, 'w', encoding='utf-8')
	with codecs.open(SourseFile, 'r', encoding='utf8') as f:
		for line in f:
			lines = line.split('\t')
			flag = False
			for word in lines[1]:
				if word >= 'a' and word <= 'z' or word >= 'A' and word <= 'Z':
					flag = True
					break
			if flag:
				ENGLISH.write(line)
			else:
				CHINESE.write(line)
	CHINESE.close()
	ENGLISH.close()

#cut('test.txt','1.txt','2.txt')

if __name__ == '__main__':
	if len(sys.argv) != 4:
		raise ValueError("""usage: python run_cnn.py SourseFile ChineseFile, EnglishFile""")
	print('/' + sys.argv[1])
	if not os.path.exists('/' + sys.argv[1]):
		raise ValueError("""usage: SourseFile can not find, please check it""")
	cut(sys.argv[1], sys.argv[2], sys.argv[3])
	print('Over')
    

