from __future__ import division
import csv, nltk, numpy, pandas as pd
from collections import Counter
from sklearn.externals import joblib
numpy.set_printoptions(suppress=True)


def transition(filename, data, tag_column):
    """
    fungsi menghitung matriks transisi dari data train berlabel postag.
    :param filename: file berupa txt dengan separator tab, kolom pertama 'kata' kolom kedua 'postag', separator kalimat enter
    :param tag_column: indeks kolom yang ingin diprediksi
    :return: matrix berupa dataframe, nama string pickel dr matrix, nilai state
    """
    data = data.applymap(str.lower)

    # simpan index "start" muncul dari kolom tag
    tag = list(data[tag_column])
    list_start = [i for i, x in enumerate(tag) if x == "start"]

    # bikin bigram untuk setiap kalimat yg dipisahkan dengan start
    bigram_tag = []
    for i in range(len(list_start)-1):
        bigram_tag.extend([' '.join(w) for w in list(nltk.ngrams(tag[list_start[i]:list_start[i+1]], 2))])

    unigram_count = Counter(tag)
    bigram_count = Counter(bigram_tag)

    # prob transisi
    transisi = {}
    for item in bigram_count.keys():
        transisi[item] = bigram_count[item] / unigram_count[item.split()[0]]

    # list state, sbg header matriks transisi
    state2 = list(set([item for item in tag if item !="start"]))
    state = ["start"]
    state.extend(state2)

    fra = []
    nilai = []
    for i in range(len(state)):
        frame = []
        nilae = []
        for j in range(1,len(state)):
            bigram = state[i] + " " + state[j]
            val = transisi.get(bigram, 0)
            frame.append(bigram)
            nilae.append(val)
        fra.append(frame)
        nilai.append(nilae)

    empty_trans = numpy.zeros(shape = (len(state), len(state)-1))
    for i in range(len(nilai)):
        empty_trans[i] = nilai[i]

    matrix_transisi = pd.DataFrame(data = empty_trans,
                 index = numpy.array(state, dtype='|S10'),
                 columns = numpy.array(state[1:], dtype='|S10'))

    pickel = filename.replace(".txt","") + '_transition.pkl'
    joblib.dump(matrix_transisi, pickel)
    return [matrix_transisi, pickel, state]


def emission(filename, data, state, tag_column):
    """
    fungsi menghitung matriks emission dari data train berlabel postag.
    :param filename: file berupa txt dengan separator tab, kolom pertama 'kata' kolom kedua 'postag', separator kalimat enter
    :param state: nilai state unik dr olahan transisi
    :param tag_column: indeks kolom yg ingin diprediksi
    :return: matrix berupa dataframe, nama string pickel dr matrix
    """
    # data_bersih = pd.read_csv(filename, sep, header = None, skip_blank_lines = True, quoting=csv.QUOTE_NONE)
    data = data[data[0] != "start"].reset_index().drop("index", 1)

    data_emission = data.applymap(str.lower)
    data_emission["frase_emission"] = data_emission[tag_column-1] + " " + data_emission[tag_column]

    statecount = Counter(list(data_emission[tag_column]))
    bigram_count = Counter(list(data_emission["frase_emission"]))

    emission = {}
    for item in bigram_count.keys():
        n = item.split()
        emission[item] = bigram_count[item] / statecount[n[len(n)-1]]

    # unik kata
    kata = list(set(list(data_emission[tag_column-1])))

    fra = []
    nilai = []
    for i in range(1,len(state)):
        frame = []
        nilae = []
        for j in range(len(kata)):
            bigram = kata[j] + " " + state[i]
            val = emission.get(bigram, 0)
            frame.append(bigram)
            nilae.append(val)
        fra.append(frame)
        nilai.append(nilae)

    empty_emission = numpy.zeros(shape = (len(state)-1, len(kata)))
    for i in range(len(nilai)):
        empty_emission[i] = nilai[i]

    matrix_emission = pd.DataFrame(data = empty_emission,
                 index = numpy.array(state[1:], dtype='|S10'),
                 columns = numpy.array(kata, dtype='|S20'))

    pickel = filename.replace(".txt","") + '_emission.pkl'
    joblib.dump(matrix_emission, pickel)

    return [matrix_emission, pickel]


def daframe_em3(column_dict, row_dict, frase_dict):
    """
    fungsi untuk mengubah hasil perhitungan probabilitas menjadi numpy ndarray dengan nama kolom dan row yang bersesuaian.
    :param column_dict: dictionary dari sebuah list yg akan dijadikan dari nama kolom
    :param row_dict: dictionary dari sebuah list yg akan dijadikan nama row
    :param frase_dict: dictionary dari kombinasi row-column berupa frase untuk assign value prob yang sesuai
    :return: matriks yang akan dipickel
    """
    tag = column_dict.keys()
    ner = row_dict.keys()

    fra = []
    nilai = []
    for i in range(len(ner)):
        frame = []
        nilae = []
        for j in range(len(tag)):
            bigram = tag[j] + " " + ner[i]
            val = frase_dict.get(bigram, 0)
            frame.append(bigram)
            nilae.append(val)
        fra.append(frame)
        nilai.append(nilae)

    empty = numpy.zeros(shape=(len(ner), len(tag)))
    for i in range(len(nilai)):
        empty[i] = nilai[i]

    matrix = pd.DataFrame(data=empty,
                                   index=numpy.array(ner, dtype='|S10'),
                                   columns=numpy.array(tag, dtype='|S20'))
    return matrix


def emission3(filename, data, tag_column):
    """
    fungsi untuk membuat-menghitung dan membentuk-matriks emisi dengan tiga perhitungan prev-cur-next
    :param filename: nama file train
    :param tag_column: indeks kolom dari dataframe yg akan diprediksi
    :return: list ketiga matriks dalam bentuk dataframe, list nama pickel dari matriks
    """

    df = data
    df = df[df[0] != "start"].reset_index().drop("index", 1)

    df = df.applymap(str.lower)

    # data disimpan di dict akan lebih cepat drpd akses langsung df
    dict_tag = {}
    dict_ner = {}
    for i in range(len(df)):
        dict_tag[i] = df[tag_column-1][i]
        dict_ner[i] = df[tag_column][i]
    count_tag = Counter(dict_tag.values())
    count_ner = Counter(dict_ner.values())

    # previous
    prev_frasa = [dict_tag[i - 1] + " " + dict_ner[i] for i in range(1, len(df))]
    prev = Counter(prev_frasa)
    previous = {}
    for item in prev.keys():
        previous[item] = prev[item] / count_tag[item.split()[0]]

    matrix_previous = daframe_em3(count_tag, count_ner, previous)
    pickel1 = filename.replace(".txt", "") + '_emission_previous.pkl'
    joblib.dump(matrix_previous, pickel1)

    # current
    current_frasa = [dict_tag[i] + " " + dict_ner[i] for i in range(len(df))]
    cur = Counter(current_frasa)
    current = {}
    for item in cur.keys():
        current[item] = cur[item] / count_ner[item.split()[1]]

    matrix_current = daframe_em3(count_tag, count_ner, current)
    pickel2 = filename.replace(".txt", "") + '_emission_current.pkl'
    joblib.dump(matrix_current, pickel2)

    # next
    next_frasa = [dict_tag[i + 1] + " " + dict_ner[i] for i in range(len(df) - 1)]
    ne = Counter(next_frasa)
    nextt = {}
    for item in ne.keys():
        nextt[item] = ne[item] / count_ner[item.split()[1]]

    matrix_next = daframe_em3(count_tag, count_ner, nextt)
    pickel3 = filename.replace(".txt", "") + '_emission_next.pkl'
    joblib.dump(matrix_next, pickel3)

    return [[matrix_current, matrix_previous, matrix_next],
            [pickel2, pickel1, pickel3]]


def make_matrix(filename, sep, partial, tag_column, viterbi=1 ):
    """
    fungsi gabungan untuk memperoleh string pickel matriks
    :param filename: nama file train
    :param tag_column: indeks kolom dari dataframe yg akan diprediksi
    :return: pickel transisi, pickel emission
    """
    data = pd.read_csv(filename, sep, header=None, skip_blank_lines=False, quoting=csv.QUOTE_NONE).fillna("start")
    if partial != None:
        n = -1
        y = []
        for i in range(len(data)):
            if data[2][i] != "start":
                y.append(n)
            else:
                n += 1
                y.append(n)

        data["index_kalimat"] = y
        data = data.loc[data['index_kalimat'].isin(partial)][[0,1,2]]

    trans = transition(filename, data, tag_column)
    if viterbi == 1:
        em = emission(filename, data, trans[2], tag_column)
        return [trans[1], em[1]]
    elif viterbi == 3:
        em = emission3(filename, data, tag_column)
        x = [trans[1]]
        x.extend(em[1])
        return x