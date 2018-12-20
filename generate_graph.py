
# coding: utf-8


"""© 2018 Rajkumar Pujari All Rights Reserved

- Original Version

    Author: Rajkumar Pujari
    Last Modified: 10/12/2018

"""

import os
from HTMLParser import HTMLParser
import json
import numpy as np
import argparse



class GraphParser(HTMLParser):
    def init_parser(self):
        self.uid = 0
        self.tag = None
        self.curr_url = None
        self.url_dict = {}
        self.url_dict_reverse = {}
        self.adj_list = {}
    
    def handle_starttag(self, tag, attrs):
        #Search for outgoing links in the attributes of the tags
        self.tag = tag
        for tup in attrs:
            for tok in tup:
                if type(tok) == type('string') and (tok.startswith('http://') or tok.startswith('https://')) and self.curr_url:
                    if tok.endswith('/'):
                        tok = tok[:-1]
                    tok = str(tok)
                    if tok in self.url_dict:
                        self.adj_list[self.url_dict[self.curr_url]].append(self.url_dict[tok])
                    else:
                        self.url_dict[tok] = str(self.uid)
                        self.url_dict_reverse[str(self.uid)] = tok
                        self.adj_list[self.url_dict[self.curr_url]].append(str(self.uid))
                        self.uid += 1
            
    def handle_endtag(self, tag):
        #End of tag scope
        self.tag = None
        
        #End of document
        if tag == 'DOC':
            self.curr_url = None

    def handle_data(self, data):
        if self.tag == 'docno':
            #Identify the URL of the document
            url = data.strip()
            if url.endswith('/'):
                url = url[:-1]
            url = str(url)
            self.curr_url = url
            if url not in self.url_dict:
                self.url_dict[url] = str(self.uid)
                self.url_dict_reverse[str(self.uid)] = url
                self.adj_list[str(self.uid)] = []
                self.uid += 1
            elif data.strip() not in self.adj_list:
                self.adj_list[self.url_dict[self.curr_url]] = []
        else:
            #Search for outgoing links in the document text
            toks = data.split()
            for tok in toks:
                if tok.startswith('https://') or tok.startswith('http://'):
                    if tok.endswith('/'):
                        tok= tok[:-1]
                    tok = str(tok)
                    if tok in self.url_dict:
                        self.adj_list[self.url_dict[self.curr_url]].append(self.url_dict[tok])
                    else:
                        self.url_dict[tok] = str(self.uid)
                        self.url_dict_reverse[str(self.uid)] = tok
                        self.adj_list[self.url_dict[self.curr_url]].append(str(self.uid))
                        self.uid += 1



def generate_graph(crawl_dir='/homes/cs473/cs_webcrawl/cs.purdue.HTML/'):
    #Instantiate and initialize the parser
    graph_parser = GraphParser()
    graph_parser.init_parser()
    fnames = sorted(os.listdir(crawl_dir))
    
    #Generate graph for the documents
    for fname in fnames:
        if 'html' in fname:
            f_str = open(crawl_dir + fname, 'r').read()
            if type(f_str) == type('string'):
                f_uni = unicode(f_str, errors='ignore')
                f_str = unicode.encode(f_uni)
            graph_parser.feed(f_str)
    
    return graph_parser



if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    arg_parser.add_argument('--crawl_dir', help='path to the crawl directory containing documents',
                 type=str, default='/homes/cs473/cs_webcrawl/cs.purdue.HTML/')
    
    arg_parser.add_argument('--adj_list_outpath', help='output path of the generated adjacency list file',
                 type=str, default='./adj_list.json')
    
    arg_parser.add_argument('--url_dict_outpath', help='output path of the generated URL to ID mappings file',
                 type=str, default='./url_dict.json')
    
    arg_parser.add_argument('--url_dict_reverse_outpath', help='output path of the generated ID to URL mappings file',
                 type=str, default='./url_dict_reverse.json')
    
    args = arg_parser.parse_args()
    
    graph_parser = generate_graph(args.crawl_dir)
    json.dump(graph_parser.adj_list, open(args.adj_list_outpath, 'w'))
    json.dump(graph_parser.url_dict, open(args.url_dict_outpath, 'w'))
    json.dump(graph_parser.url_dict_reverse, open(args.url_dict_reverse_outpath, 'w'))

else:
    pass

