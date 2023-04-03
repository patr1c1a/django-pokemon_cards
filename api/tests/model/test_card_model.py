from datetime import date
from django.db import IntegrityError
from django.test import TestCase
from api.models import Card, PokemonType, Expansion


class CardModelTests(TestCase):
    def test_create_card(self):
        """
        Tests that a Card can be created with all its fields.
        """
        expansion = Expansion.objects.create(name="expansion 1")
        pokemon_type1 = PokemonType.objects.create(name="type 1")
        pokemon_type2 = PokemonType.objects.create(name="type 2")
        card = Card.objects.create(
            name="card 1",
            first_edition=False,
            expansion=expansion,
            type1=pokemon_type1,
            type2=pokemon_type2,
            rarity="common",
            card_number=10,
            hp=70,
            price=29.99,
            image="/media/img/card1.jpg",
            created=date.today(),
        )
        self.assertEqual(card.name, "card 1")
        self.assertEqual(card.expansion, expansion)
        self.assertEqual(card.type1, pokemon_type1)
        self.assertEqual(card.type2, pokemon_type2)
        self.assertEqual(card.rarity, "common")
        self.assertEqual(card.created, date.today())

    def test_unique_constraint(self):
        """
        Tests that the unique constraint defined for the Card
        model is enforced when "name" matches an existing Card,
        (even if case doesn't match).
        """
        Card.objects.create(name="CARD 1")
        with self.assertRaises(IntegrityError):
            Card.objects.create(name="Card 1")

    def test_create_card_required_only(self):
        """
        Tests that a Card can be created with the required fields only.
        """
        card = Card.objects.create(name="card 1")
        self.assertEqual(card.name, "card 1")

    def test_update_card(self):
        """
        Tests that a Card name can be edited.
        """
        card = Card.objects.create(name="card 1")
        card.name = "new card name"
        card.save()
        updated_card = Card.objects.get(id=card.id)
        self.assertEqual(updated_card.name, "new card name")

    def test_delete_card(self):
        """
        Tests that Card can be deleted.
        """
        card = Card.objects.create(
            name="card 1",
        )
        card.delete()
        with self.assertRaises(Card.DoesNotExist):
            Card.objects.get(id=card.id)
