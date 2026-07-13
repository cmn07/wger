import pytest
from rest_framework.test import APIClient
from rest_framework import status
from wger.core.models import Language, License
from wger.exercises.models import Exercise, Translation, ExerciseCategory

@pytest.mark.django_db
def test_exerciseinfo_language_filter_returns_only_matching_exercises():
    client = APIClient()

    # Criar licença obrigatória (license_id=2 é o default do model Exercise)
    license_obj = License.objects.create(
        id=2,
        short_name="CC-BY-SA 4.0",
        full_name="Creative Commons Attribution Share Alike 4.0",
        url="https://creativecommons.org/licenses/by-sa/4.0/"
    )

    category = ExerciseCategory.objects.create(name="Chest")

    en_language = Language.objects.create(short_name="en", full_name="English")
    de_language = Language.objects.create(short_name="de", full_name="Deutsch")

    exercise_en = Exercise.objects.create(category=category, license=license_obj)
    Translation.objects.create(
        exercise=exercise_en,
        language=en_language,
        name="Push up",
        description="Do a push up"
    )

    exercise_de = Exercise.objects.create(category=category, license=license_obj)
    Translation.objects.create(
        exercise=exercise_de,
        language=de_language,
        name="Liegestütz",
        description="Mach einen Liegestütz"
    )

    response = client.get('/api/v2/exerciseinfo/', {'language': en_language.id})

    assert response.status_code == status.HTTP_200_OK
    results = response.json()['results']

    # Este assert FALHA intencionalmente antes da correção do viewset
    assert len(results) == 1
    assert results[0]['uuid'] == str(exercise_en.uuid)


@pytest.mark.django_db
def test_exerciseinfo_no_language_filter_returns_all_exercises():
    """Sem filtro de linguagem, todos os exercícios devem ser retornados."""
    client = APIClient()

    license_obj = License.objects.create(
        id=2,
        short_name="CC-BY-SA 4.0",
        full_name="Creative Commons Attribution Share Alike 4.0",
        url="https://creativecommons.org/licenses/by-sa/4.0/"
    )
    category = ExerciseCategory.objects.create(name="Chest")
    en_language = Language.objects.create(short_name="en", full_name="English")
    de_language = Language.objects.create(short_name="de", full_name="Deutsch")

    exercise_en = Exercise.objects.create(category=category, license=license_obj)
    Translation.objects.create(exercise=exercise_en, language=en_language, name="Push up", description="")

    exercise_de = Exercise.objects.create(category=category, license=license_obj)
    Translation.objects.create(exercise=exercise_de, language=de_language, name="Liegestütz", description="")

    response = client.get('/api/v2/exerciseinfo/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['count'] == 2


@pytest.mark.django_db
def test_exerciseinfo_language_filter_returns_empty_for_unknown_language():
    """Filtro por linguagem inexistente deve retornar lista vazia."""
    client = APIClient()

    license_obj = License.objects.create(
        id=2,
        short_name="CC-BY-SA 4.0",
        full_name="Creative Commons Attribution Share Alike 4.0",
        url="https://creativecommons.org/licenses/by-sa/4.0/"
    )
    category = ExerciseCategory.objects.create(name="Chest")
    en_language = Language.objects.create(short_name="en", full_name="English")

    exercise_en = Exercise.objects.create(category=category, license=license_obj)
    Translation.objects.create(exercise=exercise_en, language=en_language, name="Push up", description="")

    response = client.get('/api/v2/exerciseinfo/', {'language': 9999})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()['results']) == 0
