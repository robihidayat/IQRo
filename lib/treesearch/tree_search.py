#!/usr/bin/env python
# -*- coding: utf-8 -*-
#By Steve Hanov, 2011. Released to the public domain
# http://stevehanov.ca/blog/index.php?id=114

""" Google style docstrings

Modul pencarian dengan tree levenshein, by By Steve Hanov, 2011. Released to the public domain.
sudah di modivikasi, agar bisa dinamis dan hanya satu yang menjadi output.



File name: dictionary.py
Author: Robi Hidayat
Date created: 6/12/2016
Date last modified: 6/02/2017
Python Version: 2.7

"""
import difflib
stopwords = ['ML', 'MG', 'TAB', 'TABLET', 'LIQ', 'GRM', 'CAP', 'KAP', 'G', 'GR', 'GRAM']


# kamus_obat_super_lengkap corpus_obat
DICTIONARY = "dictionary/dictionary_string_match_medicine.txt"


# Keep some interesting statistics
NodeCount = 0
WordCount = 0

# The Trie data structure keeps a set of words, organized with one node for
# each letter. Each node has a branch for each letter that may follow it in the
# set of words.
class TrieNode:
    def __init__(self):
        self.word = None
        self.children = {}

        global NodeCount
        NodeCount += 1

    def insert(self, word ):
        node = self
        for letter in word:
            if letter not in node.children:
                node.children[letter] = TrieNode()

            node = node.children[letter]

        node.word = word

# read dictionary file into a trie
trie = TrieNode()
for word in open(DICTIONARY, "rt").read().split():
    WordCount += 1
    trie.insert(word)

# print "Read %d words into %d nodes" % (WordCount, NodeCount)

# The search function returns a list of all words that are less than the given
# maximum distance from the target word
def search(word, maxCost):

    # build first row
    currentRow = range(len(word) + 1 )

    results = []

    # recursively search each branch of the trie
    for letter in trie.children:
        searchRecursive(trie.children[letter], letter, word, currentRow,
            results, maxCost)
    # print maxCost
    return results


# This recursive helper is used by the search function above. It assumes that
# the previousRow has been filled in already.
def searchRecursive(node, letter, word, previousRow, results, maxCost):

    columns = len(word) + 1
    currentRow = [previousRow[0] + 1]

    # Build one row for the letter, with a column for each letter in the target
    # word, plus one for the empty string at column 0
    for column in xrange(1, columns):

        insertCost = currentRow[column - 1] + 1
        deleteCost = previousRow[column] + 1

        if word[column - 1] != letter:
            replaceCost = previousRow[ column - 1 ] + 1
        else:
            replaceCost = previousRow[ column - 1 ]

        currentRow.append( min( insertCost, deleteCost, replaceCost ) )

    # if the last entry in the row indicates the optimal cost is less than the
    # maximum cost, and there is a word in this trie node, then add it.
    if currentRow[-1] <= maxCost and node.word != None:
        results.append((node.word, currentRow[-1]))

    # if any entries in the row are less than the maximum cost, then
    # recursively search each branch of the trie
    if min(currentRow) <= maxCost:
        for letter in node.children:
            searchRecursive(node.children[letter], letter, word, currentRow,
                results, maxCost)


def faster_search(input_string):
    stacks = []
    if input_string == None or len(input_string) <=3:
        return ''
    else:
        input_string = input_string.upper()
        hasil = search(input_string, 1)
        dct = dict(hasil)
        if not hasil:
            return ''
        else:
            for k, v in dct.iteritems():
                if v == 0:
                    return k
                elif v== 1 :
                    stacks.append(k)
            kunyuk = difflib.get_close_matches(input_string,stacks,1)
            try:
                return kunyuk[0]
            except:
                pass
    pass


def query_string(input_string):
    if input_string == None:
        return ''
    # print input_string, 'input_string'
    split_string = input_string.upper().split()
    keterangan = get_keterangan(split_string)
    number_digits = ' '.join([s for s in split_string if s.isdigit()])
    no_integers = [x for x in split_string if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]
    no_integers = [row for row in no_integers if row not in keterangan]
    # print no_integers, 'string process to fast search'
    hasil_serching = map(lambda x:faster_search(x), no_integers)
    filter_bersih = filter(lambda x: x != '', hasil_serching)
    # print filter_bersih, ' hasil filter', type(filter_bersih)
    if not filter_bersih:
        join_filter = ''
    else:
        join_filter = ','.join(str(v) for v in filter_bersih)
    results = join_filter + ' ' + number_digits
    if not keterangan:
        return results
    if len(filter_bersih) == 0 and len(keterangan) != 0:
        pass
        # print 'Nope'
    else:
        keteranganbaru = ' '.join(keterangan)
        final_string = results + ' ' + keteranganbaru
        if all(item.isdigit() for item in final_string.split()) == True:
            return ''
        return final_string


def get_keterangan(lists):
    try:
        stacks = []
        qwert_stop_words = stopword_kamus()
        for row in lists:
            if row in stopwords or row in qwert_stop_words:
                stacks.append(row)
        return stacks
    except:
        pass


def stopword_kamus():
    kamus = "dictionary/dictionary_stopwords.txt";
    WordCount = 0
    stacks =[]
    for word in open(kamus, "rt").read().split():
        WordCount += 1
        stacks.append(word)
    return stacks


