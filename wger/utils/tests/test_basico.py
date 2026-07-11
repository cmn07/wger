# Django
from django.test import TestCase


class TestBasico(TestCase):
    def test_soma_simples(self):
        self.assertEqual(1 + 1, 2)
