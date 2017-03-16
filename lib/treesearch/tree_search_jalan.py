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
from lib.fulltextsearch.dictionary_shop import clean_shop, cleanshing_data
# kamus_obat_super_lengkap corpus_obat
DICTIONARY = "dictionary/dictionary_string_match_address.txt"


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
    trie.insert(word.upper())

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

        currentRow.append(min(insertCost, deleteCost, replaceCost ) )

    # if the last entry in the row indicates the optimal cost is less than the
    # maximum cost, and there is a word in this trie node, then add it.
    if currentRow[-1] <= maxCost and node.word != None:
        results.append((node.word, currentRow[-1]))

    # if any entries in the row are less than the maximum cost, then
    # recursively search each branch of the trie
    if min( currentRow ) <= maxCost:
        for letter in node.children:
            searchRecursive(node.children[letter], letter, word, currentRow,
                results, maxCost)


def query_jalan(input_string):
    if input_string == None:
        return ''
    input_string = clean_shop(cleanshing_data(input_string))
    split_string = input_string.upper().split()
    st1 = []
    for item in split_string:
        st = []
        res = search(item, 1)
        if len(res) != 0:
            for i, j in enumerate(res):
                if j[1] == 0:
                    st.append(j[0])
                    # print "dist 0: ", j[0]
            if len(st) == 0:
                st.append(res[0][0])
                # print "dist 1: ",res[0][0]
        st1.extend(st)
    return " ".join(st1)

