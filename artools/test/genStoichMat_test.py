
import sys
sys.path.append('../')
from artools import genStoichMat, sameRows

import scipy as sp
import pytest


def equivalentDictionaries(x, y):
    """
    Helper function to test if dictionaries x and y share the same keys and
    values OVERALL AS A SET, but not necessarily that the key-value pairs are
    the same between x and y.
    """

    for xi in list(x.values()):
        if xi not in list(y.values()):
            return False
    for yi in list(y.values()):
        if yi not in list(x.values()):
            return False

    for xi in list(x.keys()):
        if xi not in list(y.keys()):
            return False
    for yi in list(y.keys()):
        if yi not in list(x.keys()):
            return False

    return True


class TestTuple:

    def test_1(self):

        # reactions written in tuple format
        rxn_str = ("A -> B",)

        A, d = genStoichMat(rxn_str)
        A_ref = sp.array([[-1.0],
                          [1.0]])
        d_ref = {'A':0,
                 'B':1}

        assert (sameRows(A, A_ref) and equivalentDictionaries(d, d_ref) is True)


class TestNormal:

    def test_vdv3D(self):

        rxn_str = ["A -> B",
                   "B -> C",
                   "2*A -> D"]

        A, d = genStoichMat(rxn_str)
        A_ref = sp.array([[-1., 0, -2],
                          [1, -1, 0],
                          [0, 1, 0],
                          [0, 0, 1]])
        d_ref = {'A':0,
                 'B':1,
                 'C':2,
                 'D':3}

        assert (sameRows(A, A_ref) and equivalentDictionaries(d, d_ref) is True)


    def test_BTX(self):
        rxns = ['B + 0.5*E -> T',
                'T + 0.5*E -> X',
                '2*B -> D + H']

        A_ref = sp.array([[-1.0, 0.0, -2.0],
                          [-0.5, -0.5, 0.0],
                          [1.0, -1.0, 0.0],
                          [0.0, 1.0, 0.0],
                          [0.0, 0.0, 1.0],
                          [0.0, 0.0, 1.0]])
        d_ref = {'B':0,
                 'E':1,
                 'T':2,
                 'X':3,
                 'D':4,
                 'H':5}

        A, d = genStoichMat(rxns)

        assert (sameRows(A, A_ref) and equivalentDictionaries(d, d_ref) is True)


    def test_1(self):

        rxn_str = ["A -> B"]

        A, d = genStoichMat(rxn_str)
        A_ref = sp.array([[-1.0],
                          [1.0]])
        d_ref = {'A':0,
                 'B':1}

        assert (sameRows(A, A_ref) and equivalentDictionaries(d, d_ref) is True)


    def test_3(self):

        rxn_str = ['A + 2*B -> 1.5*C',
                   'A + C -> 0.5*D',
                   'C + 3.2*D -> E + 0.1*F']

        A, d = genStoichMat(rxn_str)
        A_ref = sp.array([[-1., -1, 0],
                          [-2, 0, 0],
                          [1.5, -1, -1],
                          [0, 0.5, -3.2],
                          [0, 0, 1],
                          [0, 0, 0.1]])
        d_ref = {'A':0,
                 'B':1,
                 'C':2,
                 'D':3,
                 'E':4,
                 'F':5}

        assert (sameRows(A, A_ref) and equivalentDictionaries(d, d_ref) is True)


class TestRealistic:

    def test_NH3_1(self):
        rxn = ["N2 + 3*H2 -> 2*NH3"]

        A_ref = sp.array([[-1.0, -3.0, 2.0]]).T
        d_ref = {'N2':0,
                 'H2':1,
                 'NH3': 2}
        A, d = genStoichMat(rxn)

        assert (sameRows(A, A_ref) and equivalentDictionaries(d, d_ref) is True)


    def test_CH4_reform(self):
        rxns = ['CH4 + H2O -> CO + 3*H2',
                'CO + H2O -> CO2 + H2']

        A_ref = sp.array([[-1.0, 0.0],
                          [-1.0, -1.0],
                          [1.0, -1.0],
                          [3.0, 1.0],
                          [0.0, 1.0]])
        d_ref = {'CH4':0,
                 'H2O':1,
                 'CO':2,
                 'H2':3,
                 'CO2':4}
        A, d = genStoichMat(rxns)

        assert (sameRows(A, A_ref) and equivalentDictionaries(d, d_ref) is True)


    def test_UCG_1(self):
        rxns = ['C + O2 -> CO2',
                'C + CO2 -> 2*CO',
                'CO + 0.5*O2 -> CO2',
                'C + H2O -> CO + H2',
                'CO + H2O -> CO2 + H2',
                'CO2 + H2 -> CO + H2O',
                'C + 2*H2 -> CH4',
                'CH4 + H2O -> CO + 3*H2',
                'CO + 3*H2 -> CH4 + H2O']

        A_ref = sp.array([[-1., -1, 0, -1, 0, 0, -1, 0, 0],
                          [-1, 0, -0.5, 0, 0, 0, 0, 0, 0],
                          [1, -1, 1, 0, 1, -1, 0, 0, 0],
                          [0, 2, -1, 1, -1, 1, 0, 1, -1],
                          [0, 0, 0, -1, -1, 1, 0, -1, 1],
                          [0, 0, 0, 1, 1, -1, -2, 3, -3],
                          [0, 0, 0, 0, 0, 0, 1, -1, 1]])
        d_ref = {'C':0,
                 'O2':1,
                 'CO2':2,
                 'CO':3,
                 'H2O':4,
                 'H2':5,
                 'CH4':6}
        A, d = genStoichMat(rxns)

        assert (sameRows(A, A_ref) and equivalentDictionaries(d, d_ref) is True)


    def test_formic_acid(self):
        rxns = ['HCHO + 0.5*O2 -> HCOOH',
                '        HCOOH -> CO + H2O',
                '       2*HCHO -> HCOOCH3',
                '      HCOOCH3 -> CH3OH + HCOOH']

        A_ref = sp.array([[-1. ,  0. , -2. ,  0. ],
                          [-0.5,  0. ,  0. ,  0. ],
                          [ 1. , -1. ,  0. ,  1. ],
                          [ 0. ,  1. ,  0. ,  0. ],
                          [ 0. ,  1. ,  0. ,  0. ],
                          [ 0. ,  0. ,  1. , -1. ],
                          [ 0. ,  0. ,  0. ,  1. ]])

        d_ref = {'HCHO': 0,
                 'O2': 1,
                 'HCOOH': 2,
                 'CO': 3,
                 'H2O': 4,
                 'HCOOCH3': 5,
                 'CH3OH': 6}

        A, d = genStoichMat(rxns)

        assert (sameRows(A, A_ref) and equivalentDictionaries(d, d_ref) is True)


class TestWords:

    def test_1(self):
        rxns = ['ethylene + 0.5*oxygen -> ethylene_oxide',
                'ethylene + 3*oxygen -> 2*carbon_dioxide + 2*water']

        A_ref = sp.array([[-1. , -1. ],
                          [-0.5, -3. ],
                          [ 1. ,  0. ],
                          [ 0. ,  2. ],
                          [ 0. ,  2. ]])
        d_ref = {'carbon_dioxide': 3,
                 'ethylene': 0,
                 'ethylene_oxide': 2,
                 'oxygen': 1,
                 'water': 4}

        A, d = genStoichMat(rxns)

        assert (sameRows(A, A_ref) and equivalentDictionaries(d, d_ref) is True)


class TestAutocatalytic:
    def test_1(self):
        r = "A + B -> 2*B"
        A, d = genStoichMat([r])

        A_ref = sp.array([[-1.0, 1.0]]).T
        d_ref = {'A': 0, 'B': 1}

        assert (sameRows(A, A_ref) is True)
        assert (equivalentDictionaries(d, d_ref) is True)


    def test_2(self):
        rxns = ["A + B -> 2*B",
                "A + C -> D"]
        A, d = genStoichMat(rxns)

        A_ref = sp.array([[-1., -1.],
                          [ 1.,  0.],
                          [ 0., -1.],
                          [ 0.,  1.]])
        d_ref = {'A': 0,
                 'B': 1,
                 'C': 2,
                 'D': 3}

        assert (sameRows(A, A_ref) is True)
        assert (equivalentDictionaries(d, d_ref) is True)


    def test_3(self):
        rxns = ["A + B -> 2*B",
                "B + C -> 3*C"]
        A, d = genStoichMat(rxns)

        A_ref = sp.array([[-1.,  0.],
                          [ 1., -1.],
                          [ 0.,  2.]])
        d_ref = {'A': 0,
                 'B': 1,
                 'C': 2}

        assert (sameRows(A, A_ref) is True)
        assert (equivalentDictionaries(d, d_ref) is True)


class TestErorr:

    def test_double_arrow(self):
        with pytest.raises(SyntaxError):
            rxns = ['A -> B -> C']
            genStoichMat(rxns)
