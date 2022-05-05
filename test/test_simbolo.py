from string import ascii_lowercase
from unittest import TestCase

from classes import Simbolo

class TestSimbolo(TestCase):
    def test_equality(self):
        for letra in ascii_lowercase:
            l1 = Simbolo(letra)
            l2 = Simbolo(letra)
            
            self.assertTrue(l1 == l2, '__eq__ override')
            self.assertTrue(hash(l1) == hash(l2), '__hash__ override')

        self.assertFalse(Simbolo('a') == 'a')
        self.assertTrue(Simbolo.Vazio == Simbolo(''))

    def test_repr(self):
        self.assertTrue(repr(Simbolo('a') == "Simbolo('a')"))
        self.assertTrue(repr(Simbolo('') == "Simbolo.Vazio"))