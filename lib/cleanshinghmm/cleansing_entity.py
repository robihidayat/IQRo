#!/usr/bin/python
# -*- coding: utf-8 -*-

import hmm_predict_ver2, hmm_matrix_ver2
import numpy as np
import re
filename = "dictionary/output2_tagged.txt"
sep = "\t"



# fungsi2 train hmm
def make_train(filename, sep, partial):
    var = hmm_matrix_ver2.make_matrix(filename, sep, partial, tag_column=1, viterbi=1)
    return var
def main_hmm(var_tag, test):
    predict_tag = hmm_predict_ver2.predict_ner(var_tag[0], var_tag[1], test)
    return [item.upper() for item in predict_tag]
def run_main(test):
    return main_hmm(train, str(test).lower())

# fungsi2 cleansing pd
def clean_pd(pd):
    test = pd.str.replace('"', ' ')
    test = test.str.replace("'", " ")
    test = test.str.strip()
    test = test.replace(r'\s+', " ", regex=True).replace('', np.nan)
    test = test.fillna("none")

    return test
def merge_dosis(text):
    alist = text.split()
    leng = len(alist)
    for i in range(0, leng-1):
        if alist[i].isdigit() == True:
            for item in ["GR","MG","ML", "IU", "%"]:
                if (item in alist[i+1]) == True:
                    dosis = alist[i]+alist[i+1]
                    del(alist[i])
                    alist.insert(i, dosis)
    return " ".join(alist)

# fungsi2 rule tagging after hmm
def rule1(lista):
    try:
        i = lista.index("OBAT")
        try:
            j = lista.index("SEDIAAN")
            if (j - i) > 1:
                for ind in range(i, j):
                    lista[ind] = "OBAT"
        except:
            pass
    except:
        pass
    return lista
def rule2(lista):
    try:
        i = lista.index("SEDIAAN")
        try:
            lista[i+1]
            if lista[i+1] == "SEDIAAN":
                try:
                    lista[i+2]
                    if lista[i+2] == "SAMPAH":
                        lista[i+2] = "DOSIS"
                except:
                    pass
            elif lista[i+1] == "SAMPAH":
                lista[i+1] = "DOSIS"
        except:
            pass
    except:
        pass
    return lista
def rule3(lista):
    if (lista.count("OBAT")>1) == True:
        ind = [i for i, x in enumerate(lista) if x == "OBAT"]
        if (ind[1]-ind[0]) > 1:
            for ix in range(ind[0],ind[1]):
                lista[ix] = "OBAT"
    return lista
def rule4(lista):
    try:
        i = lista.index("SEDIAAN")
        if lista[i-1] == "SAMPAH":
            lista[i-1] = "OBAT"
    except:
        pass
    return lista

# fungsi cleansing akhir
def clean1(obat, tag):
    obat = obat.split()
    if len(tag)>=3:
        if tag[0] == "SAMPAH":
            del(obat[0])
        if tag[-1] == "SAMPAH":
            del(obat[-1])

        obat = " ".join(obat)
        return obat
    elif len(tag)==1:
        if tag[0] == "SAMPAH":
            del(obat[0])
            return ""
        return obat[0]
    return " ".join(obat)

def remove_gibberish(text):
    text = re.sub(r'[^\x00-\x7F]+', '', text) # remove non-ASCII character
    # remove symbol
    text = text.replace('+', '').replace(';','').replace('%','').replace('`','').replace('~','').replace('\\','')
    text = text.replace('*', '').replace('^', '').replace('"', '').replace('|','')
    text = text.replace('?','').replace('>','').replace('<','').replace(',', '').replace(':', '')
    text = re.sub(r'\W*\b[a-z|A-Z]{1,2}\b', '', text) # remove small word
    if len(text.split()) <= 3 and len(text) < 6:
        text = text.replace("'",'').replace("-",'').replace('.', '')
    c1 = re.findall(r'(\b.{1}\b)', text)
    c2 = re.findall(r'([\w|\d]{3,})', text)
    if len(c1) >= 1 and len(c2) == 0:
        text = ''
    # replace transliteration
    cedilla2latin = [[u'Á', u'A'], [u'á', u'a'], [u'Č', u'C'], [u'č', u'c'], [u'Š', u'S'], [u'š', u's']]
    tr = dict([(a[0], a[1]) for (a) in cedilla2latin])
    new_line = ""
    for letter in text:
        if letter in tr:
            new_line += tr[letter]
        else:
            new_line += letter
    text = new_line
    # recursive cleansing symbol ,-.
    while True:
        last_text = text
        text = ' '.join([word.replace("'",'').replace("-",'').replace('.', '') if len(word) < 3 else word for word in text.split()]) # remove lonely symbol
        if text == last_text: break
    text = text.lstrip().rstrip()
    text = text if len(text) > 2 else None
    return text

def remove_nonascii(text):
    try:
        return text.encode("ascii","ignore")
    except:
        try:
            return unicode(text, "utf-8").encode("ascii","ignore")
        except:
            return ""

def main_this(column):

    # bagian inputin data hasil parsing
    print "---input data---"
    # test = pd.read_csv(file_test, sep=sep_test)
    test = clean_pd(column)
    testdf = test.to_frame()
    testdf["Product_Description_modif"] = testdf["Product Description"].apply(merge_dosis)

    print "---run predict entity with hmm---"
    testdf["ner_after_merging_dosis"] = testdf["Product_Description_modif"].apply(run_main)

    print "---cleansing hasil tagging---"
    listf = [rule1, rule2, rule3, rule4]
    for fungsi in listf:
        testdf["ner_after_modify_rule"] = testdf["ner_after_merging_dosis"].apply(fungsi)
    testdf.drop('ner_after_merging_dosis', axis=1, inplace=True)
    testdf_clean = testdf[["Product_Description_modif", "ner_after_modify_rule"]]

    testdf['clean'] = testdf_clean.apply(lambda x: clean1(x['Product_Description_modif'], x['ner_after_modify_rule']), axis=1)
    testdf['clean'] = testdf["clean"].apply(remove_gibberish)
    testdf['clean'] = testdf["clean"].apply(remove_nonascii)
    testdf['Product Description'] = testdf['clean']
    print "-----finish-----"
    # hasil_output = "output_hasil_cleansing.csv"
    # testdf.to_csv(hasil_output)
    # print hasil_output
    # return hasil_output
    return testdf['Product Description']

def cleansing_prodDesc(str):
    # WRITE YOUR CODE HERE
    try:
        prodDesc = merge_dosis(str)
        ner = run_main(prodDesc)
        listf = [rule1, rule2, rule3, rule4]
        for fungsi in listf:
            ner = fungsi(ner)
        clean = clean1(prodDesc, ner)
        clean = remove_gibberish(clean)
        clean = remove_nonascii(clean)
        return clean
    except:
        return ''



# print " -------------------RUN------------------------"
# print "---run training hmm---"
train = make_train(filename, sep, None)
# file_test = "test2.tsv"
# sep_test = "\t"
# main_this(file_test , sep_test)
# print cleansing_prodDesc(" ")