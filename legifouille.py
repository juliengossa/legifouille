# MIT License
#
# Copyright (c) 2023 Julien Gossa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

#!/usr/bin/env python

import json
import os
import sys
from io import StringIO
from datetime import datetime
from bs4 import BeautifulSoup
import csv
import argparse



class LEGI:
    codes_path = "./LEGI/legi/global/code_et_TNC_en_vigueur/code_en_vigueur"

    struct_article_keys = [ "num", "etat", "debut", "fin", "id" ]
    struct_article_header = struct_article_keys

    article_keys = [ "NUM", "DATE_DEBUT", "DATE_FIN", "ETAT" ]
    article_header = [ "article_"+a.lower() for a in article_keys ]
    
    lien_keys = [ "id", "typelien", "sens", "datesignatexte", "naturetexte", "numtexte", "num" ]
    lien_header = [ "lien_"+l for l in lien_keys ] + [ "lien_texte", "lien_url" ]

    def __init__(self, mode="versions"):
        self.mode = mode
        self.csvwriter = csv.writer(sys.stdout, quoting=csv.QUOTE_MINIMAL, quotechar='"', delimiter=';')
        if mode == "versions":
            self.csvwriter.writerow(["code"]+self.struct_article_header)            
        else:
            self.csvwriter.writerow(["code","num"] + self.lien_header)

        self.errwriter = csv.writer(sys.stderr, quoting=csv.QUOTE_MINIMAL, quotechar='"', delimiter=';')
        self.errwriter.writerow(["code","error","file"])

    def get_soup(self, file):
        try:
            with open(file, "r") as f:
                soup = BeautifulSoup(f.read(),features="xml")
            return soup
        except:
            self.errwriter.writerow([self.code, self.path, "Missing file", file])
            return BeautifulSoup()


    def parse_code(self, code, path):
        self.code = code
        self.path = self.codes_path+path
        self.root = self.path+"/texte/struct/"+os.listdir(self.path+"/texte/struct/")[0]
        
        self.articles = set()
        self.liens = {}

        self.parse_struct(self.root)
    
    def parse_struct(self, node, depth=0):
        #print("  "*depth + node)
        soup = self.get_soup(node)

        struct_articles = soup.findAll("LIEN_ART")
        for struct_article in struct_articles:
            struct_article_data = [ struct_article[key] for key in self.struct_article_keys ]
            if struct_article['id'] in self.articles: continue
            self.articles.add(struct_article['id'])    

            if self.mode == "versions":
                self.csvwriter.writerow([self.code] + struct_article_data)
            else: 
                liens = self.parse_article_liens(struct_article)
                
                if struct_article['num'] not in self.liens: self.liens[struct_article['num']] = set()
                
                for lien in liens:
                    if lien[0] in self.liens[struct_article['num']]: continue
                    self.liens[struct_article['num']].add(lien[0])
                    self.csvwriter.writerow([self.code,struct_article['num']] + lien)

        sections = soup.findAll("LIEN_SECTION_TA")
        for section in sections:
            self.parse_struct(self.path + "/section_ta" + section['url'], depth+1)

    def parse_article_liens(self, struct_article):
        article = self.get_article(struct_article)

        liens = []
        for lien in article.findAll("LIEN"):
            
            lien_data = [ lien[key] for key in self.lien_keys ]
            if lien_data[-2] == "": lien_data[-2] = lien.text.split(" - ")[0]
            url = "https://www.legifrance.gouv.fr/jorf/id/"+lien['cidtexte']
            liens.append(lien_data + [lien.text, url])

        return liens

    def get_article(self,struct_article):
        num = struct_article['id'].replace("LEGIARTI","").strip()
        sp = "/".join([ num[i:i+2] for i in range(0,10,2) ])

        apath = self.path + "/article/"+struct_article['origine']+"/ARTI/" + sp + "/" + struct_article['id'] + ".xml"
        return self.get_soup(apath)

code_path = {
    'éducation':"LEGI/legi/global/code_et_TNC_en_vigueur/code_en_vigueur/LEGI/TEXT/00/00/06/07/11/LEGITEXT000006071191/"
}

def root_to_path(root, path = "LEGI/legi/global/code_et_TNC_en_vigueur/code_en_vigueur"):
    return '/'.join([path, root[0:4],root[4:8], root[8:10], root[10:12], root[12:14], root[14:16], root[16:18], root])

def main():
    parser = argparse.ArgumentParser(description='Parser de la base LEGI')
    parser.add_argument('-l', '--liens', help='extrait les liens des articles en vigueur plutôt que les versions', 
                        action='store_const', dest='mode', default="versions", const="liens")
    parser.add_argument('codescsv', type=str, help='Csv file listing the codes to parse', nargs='?', default='data/fr-legi-codes-en-vigueur.csv')
    args = parser.parse_args()

    legi = LEGI(args.mode)
    with open(args.codescsv, "r") as f:
        codes = csv.DictReader(f, quotechar='"')
        for code in codes:
            try:
                legi.parse_code(code['code'], code['path'])
            except FileNotFoundError:
                legi.errwriter.writerow([code['code'], "Missing root file", code['path']])


if __name__ == "__main__":
    main()
