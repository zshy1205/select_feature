import confim as cf
import random
import codecs
import math
import re
import sys
import copy

print(cf.feature)


def add_feature(feature_dict, all_feature, metadata_feature):
	feature_length = len(metadata_feature)
	feature_width = len(metadata_feature[0])
	print(feature_length)
	print(feature_width)
	for formats in cf.feature:
		for i in range(0, feature_length):
			flag = True
			feature = ''
			for format in formats.split('|'):
				nums = format[3:-1].split(',')
				if(int(nums[1]) < 0 or int(nums[1]) >= feature_width):
					raise ValueError("""usage: wrong! please check your format""")
				#print(i + int(nums[0]))
				if i + int(nums[0]) >= 0 and i + int(nums[0]) < feature_length:
					#print "##", i + int(nums[0])
					#print nums[1]
					feature += ('_' + metadata_feature[i + int(nums[0])][int(nums[1])])
				else:
					flag = False
				#print(feature)
			if flag:
				feature = feature[1:]
				if feature in all_feature.keys():
					all_feature[feature] += 1
				else:
					all_feature[feature] = 1
				if feature in feature_dict.keys():
					feature_dict[feature] += 1
				else:
					feature_dict[feature] = 1
		

def deal_feature(line):
	lines = line.split('|')
	res = []
	for l in lines:
		features = l.split('_')
		res.append(features)
	print(res)
	return res
def analy(infile):
	all_sentences = []
	all_feature = {}
	if cf.L1:
		all_feature['L1'] = 0
	if cf.L3:
		all_feature['L3'] = 0
	with codecs.open(infile, 'r', encoding='utf-8') as fp:
		for line in fp:
			dic = {}
			lines = line.split('\t')
			dic['num'] = lines[0]
			dic['text'] = lines[1]
			dic['length'] = int(lines[5])
			metadata_feature = deal_feature(lines[2])
			feature_dict = {}
			dic['feature'] = feature_dict
			if cf.L1:
				feature_dict['L1'] = int(lines[3])
				all_feature['L1'] += int(lines[3])
			if cf.L3:
				feature_dict['L3'] = int(lines[4])
				all_feature['L3'] += int(lines[4])
			add_feature(feature_dict, all_feature, metadata_feature)
			
			#print feature_dict
			#print all_feature
			all_sentences.append(dic)
			
	return	all_sentences, all_feature



def cal(infile, min_size, max_size):
	all_sen, all_mon_dict  = analy(infile)
	print('all_mon_dict is: ', all_mon_dict)
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
	gen(all_sen_in_size, all_mon_list, mon2pos_dic, pos2mon_dic, cf.WANT_NUM)

def score(s2list, all_mon_list, mon2pos_dic):
	
	normalization_list = [0.0] * len(all_mon_list)
	add_ = 0.0
	mul_ = 0.0
	for i in range(0, len(all_mon_list)):
		normalization_list[i] = s2list[i] / all_mon_list[i]
		add_ += normalization_list[i]
		mul_ += math.pow(normalization_list[i], 2)

	static_score = math.sqrt(len(all_mon_list) - s2list.count(0.0)) / math.sqrt(len(all_mon_list))
	print("static_score: ", static_score)

	dynamic_score = add_ / math.sqrt(len(all_mon_list)) / math.sqrt(mul_)
	#print('dynamic_score: ', dynamic_score)

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
		for x,v in all_sen[pos]['feature'].items():
			if x in mon2pos_dic.keys():
				s2list[mon2pos_dic[x]] += v
	print("s2list: ", s2list)
	print(s)
	best_score = score(s2list, all_mon_list, mon2pos_dic)
	print(best_score)
	flag = True
	while flag:
		flag = False
		for change_id in range(0, all_sen_size):
			
			if change_id not in s:
				s_list = list(s)
				for choose_id in s_list:
					s2list_temp = copy.copy(s2list)
					for x,v in all_sen[change_id]['feature'].items():
						if x in mon2pos_dic.keys():
							s2list_temp[mon2pos_dic[x]] += v	
					for x,v in all_sen[choose_id]['feature'].items():
						if x in mon2pos_dic.keys():
							s2list_temp[mon2pos_dic[x]] -= v
					score_temp = score(s2list_temp, all_mon_list, mon2pos_dic)
					print("score: ", score_temp)
					if(score_temp - best_score > 0.000001):
						print('score changed!')
						flag = True
						best_score = score_temp
						s2list = s2list_temp
						s.remove(choose_id)
						s.add(change_id)
						break

	'''
	while times < cf.ITER_TIMES:
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
		for x,v in all_sen[choose_id]['feature'].items():
			if x in mon2pos_dic.keys():
				s2list_temp[mon2pos_dic[x]] -= v
		for x,v in all_sen[change_id]['feature'].items():
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
	'''
	print('run over!, the choose is:')
	print(s)
	print('the best_score is: ', best_score)
	print('the lack of feature:')
	for i in range(0,len(s2list)):
		if not s2list[i]:
			print("##", pos2mon_dic[i])
	#want output
	if cf.IF_OUTPUT_NONE_EXIST:
		pass

cal('text_copy.txt', cf.MIN_SIZE, cf.MAX_SIZE)
