import pinyin_split as ps
import codecs
import re
import random
import math

CIRCULATE_TIMES = 4

def pinyin2mon(sentence):
	pinyin_list = re.split('[0123456789]', sentence)
	#print(pinyin_list)
	res = ''
	length = 0
	for pinyin in pinyin_list[:-1]:
		res += ps.trans[pinyin]
		length += len(pinyin)
		res += sentence[length]
		length += 1
		res += '_'
	print("res: ", res)
	return res, len(pinyin_list)
def analy(infile):
	all_mon_dict={}
	all_sen=[]
	done = 0
	with codecs.open(infile, 'r', encoding='utf-8') as fp:
		while True:
			number = fp.readline()
			if number == '':
				break
			sentence = fp.readline()
			yunlv = fp.readline()
			pinyin = fp.readline()
			pos_tagging = fp.readline()
			white = fp.readline()
			dic = {}
			dic['num'] = number
			mon,dic['length'] = pinyin2mon(pinyin.strip())
			for mon_ in mon[:-1].split('_'):
				if mon_ in dic.keys():
					dic[mon_] += 1
				else:
					dic[mon_] = 1
				if mon_ in all_mon_dict.keys():
					all_mon_dict[mon_] += 1
				else:
					all_mon_dict[mon_] = 1
			all_sen.append(dic)
	return all_mon_dict, all_sen

def cal(infile, want_nums, min_size, max_size):
	all_mon_dict, all_sen = analy(infile)
	print('all sentence size is:', len(all_sen))
	print('all mon size is:', len(all_mon_dict))
	print('now cal......')
	#trans dict to list
	all_mon_list = []
	mon2pos_dic = {}
	pos2mon_dic = {}
	pos = 0
	for x,v in all_mon_dict.items():
		all_mon_list.append(v)
		mon2pos_dic[x] = pos
		pos2mon_dic[pos] = x
		pos += 1
	print(len(all_mon_list))
	print(all_mon_list)

	all_sen_in_size = []
	for dic in all_sen:
		if dic['length'] >= min_size and dic['length'] <= max_size:
			all_sen_in_size.append(dic)
	print(len(all_sen_in_size))
	gen(all_sen_in_size, all_mon_list, mon2pos_dic, pos2mon_dic, want_nums)

def score(s2list, all_mon_list, mon2pos_dic):
	
	normalization_list = [0.0] * len(all_mon_list)
	add_ = 0.0
	mul_ = 0.0
	for i in range(0, len(all_mon_list)):
		normalization_list[i] = s2list[i] / all_mon_list[i]
		add_ += normalization_list[i]
		mul_ += math.pow(normalization_list[i], 2)

	static_score = math.sqrt(s2list.count(0.0)) / math.sqrt(len(all_mon_list))

	dynamic_score = add_ / math.sqrt(3) / math.sqrt(mul_)

	static_ratio = 0.9
	return static_ratio * static_score + (1 - static_ratio) * dynamic_score

def gen(all_sen, all_mon_list, mon2pos_dic,pos2mon_dic, want_nums):
	all_mon_size = len(all_mon_list)
	all_sen_size = len(all_sen)
	s = set()
	while len(s) != want_nums:
		s.add(random.randint(0, all_sen_size - 1))
	s2list = [0.0] * len(all_mon_list)
	for pos in s:
		for x,v in all_sen[pos].items():
			if x in mon2pos_dic.keys():
				s2list[mon2pos_dic[x]] += v
	print(s)
	best_score = score(s2list, all_mon_list, mon2pos_dic)
	print(best_score)
	times = 0
	while times < CIRCULATE_TIMES:
		times += 1
		s_list = list(s)
		choose_id = s_list[random.randint(0, len(s) - 1)]
		while True:
			change_id = random.randint(0, want_nums - 1)
			if change_id in s:
				continue
			else:
				break
		s2list_temp = s2list
		for x,v in all_sen[choose_id].items():
			if x in mon2pos_dic.keys():
				s2list_temp[mon2pos_dic[x]] -= v
		for x,v in all_sen[change_id].items():
			if x in mon2pos_dic.keys():
				s2list_temp[mon2pos_dic[x]] += v
		score_temp = score(s2list_temp, all_mon_list, mon2pos_dic)
		print("time: ", times, score_temp)
		if(score_temp - best_score > 0.000001):
			print('score changed!')
			best_score = score_temp
			s2list = s2list_temp
			s.remove(choose_id)
			s.add(change_id)
	print('run over!, the choose is:')
	print(s)
	print('the lack of mon:')
	for i in range(0,len(s2list)):
		if not s2list_temp[i]:
			print(pos2mon_dic[i])



	



cal('out1.txt',4, 1, 100)
#analy('out1.txt')
#pinyin2mon('xi6ma3la1ya3sou1dao4de5jie2mu4dou1fang4bu4liao3le5dai1hui4zai4shi4shi5ba5')
