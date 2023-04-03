from django.db import IntegrityError
from django.test import TestCase
from api.models import PokemonType


class PokemonTypeModelTests(TestCase):
    def test_create_pokemontype(self):
        """
        Tests that a PokemonType can be created with all its fields.
        """
        type1 = PokemonType.objects.create(name="type 1")
        type2 = PokemonType.objects.create(name="type 2")
        type3 = PokemonType.objects.create(name="type 3")
        type4 = PokemonType.objects.create(name="type 4")
        pokemon_type = PokemonType.objects.create(name="type 5")
        pokemon_type.strong_vs.set([type1, type2])
        pokemon_type.weak_vs.set([])
        pokemon_type.resistant_to.set([type3, type4])
        pokemon_type.vulnerable_to.set([type2])
        pokemon_type_from_db = PokemonType.objects.get(id=pokemon_type.id)
        self.assertEqual(pokemon_type_from_db.name, "type 5")
        self.assertEqual(set(pokemon_type_from_db.strong_vs.all()), {type1, type2})
        self.assertEqual(set(pokemon_type_from_db.weak_vs.all()), set())
        self.assertEqual(set(pokemon_type_from_db.resistant_to.all()), {type3, type4})
        self.assertEqual(set(pokemon_type_from_db.vulnerable_to.all()), {type2})

    def test_unique_constraint(self):
        """
        Tests that the unique constraint defined for the PokemonType
        model is enforced when "name" matches an existing PokemonType
        (even if case doesn't match).
        """
        PokemonType.objects.create(name="TYPE 1")
        with self.assertRaises(IntegrityError):
            PokemonType.objects.create(name="Type 1")

    def test_create_pokemontype_required_only(self):
        """
        Tests that a PokemonType can be created with the required fields only.
        """
        pokemon_type = PokemonType.objects.create(name="type 1")
        self.assertEqual(pokemon_type.name, "type 1")

    def test_update_pokemontype(self):
        """
        Tests that a PokemonType name can be edited.
        """
        pokemon_type = PokemonType.objects.create(name="type 1")
        pokemon_type.name = "new type name"
        pokemon_type.save()
        updated_type = PokemonType.objects.get(id=pokemon_type.id)
        self.assertEqual(updated_type.name, "new type name")

    def test_delete_pokemontype(self):
        """
        Tests that a PokemonType can be deleted.
        """
        pokemon_type = PokemonType.objects.create(name="type 1")
        pokemon_type.delete()
        with self.assertRaises(PokemonType.DoesNotExist):
            PokemonType.objects.get(id=pokemon_type.id)
