from string import ascii_lowercase
from unittest import TestCase

from classes.simbolo import Simbolo

class TestSimbolo(TestCase):
    def test_equality(self):
        for letra in ascii_lowercase:
            l1 = Simbolo(letra)
            l2 = Simbolo(letra)
            
            self.assertTrue(l1 == l2)
            self.assertTrue(hash(l1) == hash(l2))