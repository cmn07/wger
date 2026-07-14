from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from wger.core.models import Language, License
from wger.exercises.models import Exercise, Translation, ExerciseCategory


class TestExerciseInfo(APITestCase):
    def setUp(self):
        """Prepara o ambiente e os dados para todos os testes da classe."""
        self.client = APIClient()
        self.license_obj = License.objects.create(id=2, short_name="CC-BY-SA 4.0",
            full_name="Creative Commons", url="https://creativecommons.org")
        self.category = ExerciseCategory.objects.create(name="Chest")
        self.en_language = Language.objects.create(short_name="en", full_name="English")
        self.de_language = Language.objects.create(short_name="de", full_name="Deutsch")

    def test_exerciseinfo_language_filter_returns_only_matching_exercises(self):
        """Garante que o filtro retorna apenas exercícios do idioma especificado."""
        exercise_en = Exercise.objects.create(category=self.category, license=self.license_obj)
        Translation.objects.create(exercise=exercise_en, language=self.en_language, name="Push up",
                                   description="Do a push up")
        exercise_de = Exercise.objects.create(category=self.category, license=self.license_obj)
        Translation.objects.create(exercise=exercise_de, language=self.de_language,
                                   name="Liegestutz", description="Mach einen Liegestutz")
        response = self.client.get('/api/v2/exerciseinfo/', {'language': self.en_language.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['uuid'], str(exercise_en.uuid))

    def test_exerciseinfo_no_language_filter_returns_all_exercises(self):
        """Sem filtro de linguagem, todos os exercícios devem ser retornados."""
        exercise_en = Exercise.objects.create(category=self.category, license=self.license_obj)
        Translation.objects.create(exercise=exercise_en, language=self.en_language, name="Push up",
                                   description="")
        exercise_de = Exercise.objects.create(category=self.category, license=self.license_obj)
        Translation.objects.create(exercise=exercise_de, language=self.de_language,
                                   name="Liegestutz", description="")
        response = self.client.get('/api/v2/exerciseinfo/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 2)

    def test_exerciseinfo_language_filter_returns_empty_for_unknown_language(self):
        """Filtro por linguagem inexistente deve retornar lista vazia."""
        exercise_en = Exercise.objects.create(category=self.category, license=self.license_obj)
        Translation.objects.create(exercise=exercise_en, language=self.en_language, name="Push up",
                                   description="")
        response = self.client.get('/api/v2/exerciseinfo/', {'language': 9999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 0)
