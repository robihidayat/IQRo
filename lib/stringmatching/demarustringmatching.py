from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance
import re


def flag(InputKamus, InputFTS):

    InputKamus = str(InputKamus)
    InputFTS = str(InputFTS)
    digits_input = ' '.join(re.findall(r'\d+', InputKamus))
    digits_fts = ' '.join(re.findall(r'\d+', InputFTS))
    no_int_kamus = ' '.join([x for x in InputKamus.split() if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())])
    no_int_fts = ' '.join([x for x in InputFTS.split() if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())])
    # try:
    if digits_input or digits_fts:
        nilai_digits = normalized_damerau_levenshtein_distance(digits_fts, digits_input)
        # print "number", nilai_digits
        # print 'DIGITS', nilai_digits
        if nilai_digits >= 0.5:
            return 'NUMBERS'
        elif nilai_digits <= 0.4:
            return 'CONFIDENT'

    if no_int_kamus or no_int_fts:
        nilai_kalimat = normalized_damerau_levenshtein_distance(no_int_kamus, no_int_fts)
        # print "word", nilai_kalimat
        # print 'KATA', nilai_kalimat
        if nilai_kalimat >= 0.5:
            return 'WORDS'
        elif nilai_kalimat <= 0.4:
            return 'CONFIDENT'

def normalisasi(inputstring):
    pattern = re.compile('[^A-Za-z0-9]+')
    InputKamus = pattern.sub(' ', inputstring)
    parts = re.split('(\d+)', InputKamus)
    return ' '.join(parts)

# fts,parsing
def flag_demaru(InputKamus, InputFTS):

    if InputKamus == 'NOT FOUND' and InputFTS:
        return 'NOT CONFIDENT'
    elif InputKamus == 'NOT FOUND' and not InputFTS:
        return 'NOT FOUND'
    elif InputKamus == None:
        return 'NOT FOUND'

    data = flag(normalisasi(InputKamus), normalisasi(InputFTS))
    # print data
    if data:
        return data
    else:
        return 'NOT FOUND'

def flag_na_n_ad(InputKamus, InputFTS):

    InputKamus = str(InputKamus)
    InputFTS = str(InputFTS)
    digits_input = ' '.join(re.findall(r'\d+', InputKamus))
    digits_fts = ' '.join(re.findall(r'\d+', InputFTS))
    no_int_kamus = ' '.join([x for x in InputKamus.split() if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())])
    no_int_fts = ' '.join([x for x in InputFTS.split() if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())])
    # try:
    if digits_input or digits_fts:
        nilai_digits = normalized_damerau_levenshtein_distance(digits_fts, digits_input)
        # print "number", nilai_digits
        # print 'DIGITS', nilai_digits
        if nilai_digits >= 0.5:
            return 'CONFIDENT'
        elif nilai_digits <= 0.4:
            return 'CONFIDENT'

    if no_int_kamus or no_int_fts:
        nilai_kalimat = normalized_damerau_levenshtein_distance(no_int_kamus, no_int_fts)
        # print "word", nilai_kalimat
        # print 'KATA', nilai_kalimat
        if nilai_kalimat >= 0.5:
            return 'CONFIDENT'
        elif nilai_kalimat <= 0.4:
            return 'CONFIDENT'

def flag_demaru_name_n_addres(InputKamus, InputFTS):

    if InputKamus == 'NOT FOUND' and InputFTS:
        return 'NOT CONFIDENT'
    elif InputKamus == 'NOT FOUND' and not InputFTS:
        return 'NOT FOUND'
    elif InputKamus == None:
        return 'NOT FOUND'

    data = flag_na_n_ad(normalisasi(InputKamus), normalisasi(InputFTS))
    # print data
    if data:
        return data
    else:
        return 'NOT FOUND'


