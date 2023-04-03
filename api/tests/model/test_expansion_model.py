from django.test import TestCase
from api.models import Expansion
from datetime import date
from django.db import IntegrityError


class ExpansionModelTests(TestCase):
    def test_create_expansion(self):
        """
        Tests that an Expansion can be created with all its fields.
        """
        expansion = Expansion.objects.create(
            name="expansion 1",
            series="series 1",
            cards=100,
            release_date=date.today(),
            promotional_set=False,
        )
        self.assertEqual(expansion.name, "expansion 1")
        self.assertEqual(expansion.series, "series 1")
        self.assertEqual(expansion.cards, 100)
        self.assertEqual(expansion.release_date, date.today())
        self.assertFalse(expansion.promotional_set)

    def test_unique_constraint(self):
        """
        Tests that the unique constraint defined for the Expansion model
        is enforced when both "name" and "series" match an existing
        Expansion (even if case doesn't match).
        """
        Expansion.objects.create(name="EXPANSION 1", series="SERIES 1")
        with self.assertRaises(IntegrityError):
            Expansion.objects.create(name="expansion 1", series="series 1")

    def test_unique_constraint_with_different_series(self):
        """
        Tests that no IntegrityError is raised when the name matches
        an existing Expansion but the series does not (even if case doesn't match).
        """
        Expansion.objects.create(name="EXPANSION 1", series="series 1")
        try:
            Expansion.objects.create(name="expansion 1", series="other series")
        except IntegrityError:
            self.fail("IntegrityError raised when series is different")

    def test_unique_constraint_with_different_name(self):
        """
        Tests that no IntegrityError is raised when the series matches
        an existing Expansion but the name does not (even if case doesn't match).
        """
        Expansion.objects.create(name="expansion 1", series="SERIES 1")
        try:
            Expansion.objects.create(name="other name", series="series 1")
        except IntegrityError:
            self.fail("IntegrityError raised when name is different")

    def test_create_expansion_required_only(self):
        """
        Tests that an Expansion can be created with the required fields only.
        """
        expansion = Expansion.objects.create(name="expansion 1", series="series 1")
        self.assertEqual(expansion.name, "expansion 1")
        self.assertEqual(expansion.series, "series 1")

    def test_update_expansion(self):
        """
        Tests that an Expansion name can be edited.
        """
        expansion = Expansion.objects.create(
            name="expansion 1",
            series="series 1",
            cards=100,
            release_date="2022-01-01",
            promotional_set=False,
        )
        expansion.name = "new expansion name"
        expansion.save()
        updated_expansion = Expansion.objects.get(id=expansion.id)
        self.assertEqual(updated_expansion.name, "new expansion name")

    def test_delete_expansion(self):
        """
        Tests that an Expansion can be deleted.
        """
        expansion = Expansion.objects.create(
            name="Expansion 1",
            series="Series 1",
            cards=100,
            release_date="2022-01-01",
            promotional_set=False,
        )
        expansion.delete()
        with self.assertRaises(Expansion.DoesNotExist):
            Expansion.objects.get(id=expansion.id)
