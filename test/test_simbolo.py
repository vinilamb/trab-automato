from unittest import TestCase

from classes import Simbolo

class TestSimbolo(TestCase):
    def test_equals_operator_equality(self):
        self.assertTrue(Simbolo('a') == Simbolo('a'))

    def test_same_value_same_hash(self):
        self.assertTrue(hash(Simbolo('a')) == hash(Simbolo('a')))

    def test_repr(self):
        self.assertTrue(repr(Simbolo('a') == "Simbolo('a')"))
    
    def test_repr_empty(self):    
        self.assertTrue(repr(Simbolo('') == "Simbolo.Vazio"))