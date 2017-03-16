from __future__ import division
import hmm_viterbi, numpy as np
from sklearn.externals import joblib


def predict_ner(matrix_transisi, matrix_emisi_cur, test, matrix_emisi_prev=None, matrix_emisi_next=None):
    """
    fungsi untuk memprediksi nilai ner atau tag dari sekuens data test
    :param matrix_transisi: matriks transisi
    :param matrix_emisi_cur: matriks emisi current observation
    :param test: string test case tiap unit dipisah spasi
    :param matrix_emisi_prev: matriks emisi previous
    :param matrix_emisi_next: matriks emisi next
    :return: list hasil prediksi
    """
    """ matrix transition dan emission/obs likelihood """
    Apandas = joblib.load(matrix_transisi)
    A = np.array(Apandas)

    emission = joblib.load(matrix_emisi_cur)
    test = test.split()
    header = list(emission.columns.values)
    notin = list(set([item for item in test if item not in header]))

    if len(notin) != 0:
        for item in notin:
            prob = test.count(item) / len(test)
            emission[item] = 0.000000
            emission.ix["sampah", item] = prob

    Bpandas = emission[test]

    statenames = Bpandas.index.tolist()
    B = np.array(Bpandas)

    trans = A[1:, :]
    pi = np.expand_dims(np.array(A[0, :]), 1)

    if (matrix_emisi_prev != None and matrix_emisi_next != None):
        prev = joblib.load(matrix_emisi_prev)
        next = joblib.load(matrix_emisi_next)

        Cpandas = prev[test]
        C = np.array(Cpandas)

        Dpandas = next[test]
        D = np.array(Dpandas)

        decoder = hmm_viterbi.Decoder(pi, trans, B, C, D)  # ini bagian assign atribut objek
        states = decoder.Decode(np.arange(len(Bpandas.columns)))
    else:
        decoder = hmm_viterbi.Decoder(pi, trans, B)
        states = decoder.Decode_base(np.arange(len(Bpandas.columns)))
    """ do the decoding """
    result = np.array(statenames)[states].tolist()

    return result
