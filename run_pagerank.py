import numpy as np 
import json
import argparse
import scipy.sparse.linalg as E
import scipy.linalg as sc
import time

if __name__ == '__main__':
	start_time = time.time()
	arg_parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	arg_parser.add_argument('--adj_list', help='path to the adjacency list file (JSON)',
                 type=str, default='/homes/cs473/project2/adj_list.json')

	arg_parser.add_argument('--k', help='number of hubs and authorities (top-k) for which the scores should be printed',
                 type=int, default=5)

	arg_parser.add_argument('--url_dict_reverse', help='path to ID to URL mapping file (JSON)',
                 type=str, default='/homes/cs473/project2/url_dict_reverse.json')

	args = arg_parser.parse_args()
  
	adj_list = json.load(open(args.adj_list, 'r'))
	url_dict_reverse = json.load(open(args.url_dict_reverse, 'r'))
	#print url_dict_reverse

 	M = np.zeros([6667,6667])

	#print adj_list
	for n1 in adj_list:
		#print n1
		i = int(n1)
		#print i
		for n2 in adj_list[n1]:
			#print adj_list[n1]
			if len(adj_list[n1]) > 0:
				M[i][int(n2)] = 1
			#else:
			#	pass
	#print M
	count = 1
	B = np.zeros([6667,6667])
	for j in range(len(M)):
		#if M[j]
		if str(j) in adj_list:
			count = M[j].sum()
			#print count
			for k in range(len(M[j])):
				if(count!=0):
					B[j][k] = M[j][k] * (1.0/count)
				else:
					pass
	#print B
	B_t = np.transpose(B)
	#print B_t

	val, vector = E.eigs(B_t, k = args.k, which = 'LM')
	#val, vector = sc.eig(B_t)
	maxVal = np.abs(val).max();
	#PageRank = np.where(val == maxVal)
	#print (np.dot(vector[np.argmax(val)], B_t))
	#c = 1/val
	#print val
	#print max(val)
	#print np.argmax(val)
	#e = []
	#for v in vector:
	#	e.append(vector[0])
	ranks = vector[np.argmax(val)]
	#for i in ranks:
		#round()
	ranks = np.absolute(ranks)
	dictOfWords = {i : ranks[i] for i in range(0, len(ranks))}
	# print dictOfWords
	# print dictOfWords
	#dictOfWords_new = [(url_dict_reverse[str(id_)], round(dictOfWords[id_], 10)) for id_ in dictOfWords]
	dictOfWords_new = [(url_dict_reverse[str(id_)], "{:.16f}".format(float(dictOfWords[id_]))) for id_ in dictOfWords]

	sorted_dictOfWords = sorted(dictOfWords_new, key=lambda kv: kv[1], reverse = True)
	#print sorted_dictOfWords
	for tup in sorted_dictOfWords[:args.k]:
            print(str(tup[1]) + '\t' + tup[0])
	print("--- %s seconds ---" % (time.time() - start_time))
else:
	pass