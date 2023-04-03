from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Card, Expansion, PokemonType
from api.serializers import CardSerializer
from datetime import date


class CardListTests(APITestCase):
    def setUp(self):
        self.card1 = Card.objects.create(
            name="card 1",
            rarity="common",
            expansion=None,
            type1=None,
            type2=None,
            hp=None,
            card_number=None,
            price=None,
            image=None,
        )
        self.card2 = Card.objects.create(
            name="card 2",
            rarity="rare",
            expansion=None,
            type1=None,
            type2=None,
            hp=None,
            card_number=None,
            price=None,
            image=None,
        )

    def test_list_cards(self):
        """
        Tests that all cards are returned by the view.
        """
        url = reverse("card-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = CardSerializer([self.card1, self.card2], many=True).data
        self.assertEqual(response.data["results"], serialized_data)

    def test_filter_by_name(self):
        """
        Tests that the view returns only the cards with the given name.
        """
        url = reverse("card-list")
        response = self.client.get(url, {"search": "card 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = CardSerializer([self.card1], many=True).data
        self.assertEqual(response.data["results"], serialized_data)

    def test_filter_by_rarity(self):
        """
        Tests that the view returns only the cards with the given rarity.
        """
        url = reverse("card-list")
        response = self.client.get(url, {"search": "rare"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = CardSerializer([self.card2], many=True).data
        self.assertEqual(response.data["results"], serialized_data)

    def test_filter_by_date(self):
        """
        Tests that the view returns only the cards created on the given date.
        """
        url = reverse("card-list")

        # Use a past date (no cards exist)
        response = self.client.get(
            url, {"created__year": 1990, "created__month": 10, "created__day": 15}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

        # Use the current date and test again
        response = self.client.get(
            url,
            {
                "created__year": date.today().year,
                "created__month": date.today().month,
                "created__day": date.today().day,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)


class CardDetailTests(APITestCase):
    def setUp(self):
        self.card1 = Card.objects.create(
            name="card 1",
            rarity="common",
            expansion=None,
            type1=None,
            type2=None,
            hp=None,
            card_number=None,
            price=None,
            image=None,
        )
        self.card2 = Card.objects.create(
            name="card 2",
            rarity="rare",
            expansion=None,
            type1=None,
            type2=None,
            hp=None,
            card_number=None,
            price=None,
            image=None,
        )

    def test_get_card_by_id(self):
        """
        Tests that a card can be retrieved by its ID.
        """
        url = reverse("card-by-id", args=[self.card1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = CardSerializer(self.card1).data
        self.assertEqual(response.data, serialized_data)

    def test_delete_card_by_id(self):
        """
        Tests that a card can be deleted by its ID.
        """
        url = reverse("card-by-id", args=[self.card1.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Card.DoesNotExist):
            Card.objects.get(pk=self.card1.pk)

    def test_get_non_existent_card_by_id(self):
        """
        Tests that a non-existent card cannot be retrieved by its ID.
        """
        url = reverse("card-by-id", args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existent_card_by_id(self):
        """
        Tests that a non-existent card cannot be deleted by its ID.
        """
        url = reverse("card-by-id", args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_card(self):
        """
        Tests the name field of an existing card can be updated by PATCH.
        """
        url = reverse("card-by-id", args=[self.card1.id])
        data = {"name": "new name"}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.card1.refresh_from_db()
        self.assertEqual(self.card1.name, "new name")


class CardFilterByExpansionTests(APITestCase):
    def setUp(self):
        self.expansion1 = Expansion.objects.create(name="expansion 1", release_date=date.today())
        self.expansion2 = Expansion.objects.create(name="expansion 2", release_date=date.today())
        self.card1 = Card.objects.create(
            name="card 1",
            rarity="common",
            expansion=self.expansion1,
            type1=None,
            type2=None,
            hp=None,
            card_number=None,
            price=None,
            image=None,
        )
        self.card2 = Card.objects.create(
            name="card 2",
            rarity="rare",
            expansion=self.expansion1,
            type1=None,
            type2=None,
            hp=None,
            card_number=None,
            price=None,
            image=None,
        )
        self.card3 = Card.objects.create(
            name="card 3",
            rarity="common",
            expansion=self.expansion2,
            type1=None,
            type2=None,
            hp=None,
            card_number=None,
            price=None,
            image=None,
        )

    def test_filter_by_expansion(self):
        """
        Tests that the view returns only the cards with the given expansion.
        """
        url = reverse("card-list-by-expansion", kwargs={"pk": self.expansion1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serialized_data = CardSerializer([self.card1, self.card2], many=True).data
        self.assertEqual(response.data["results"], serialized_data)

    def test_filter_by_nonexistent_expansion(self):
        """
        Tests that the view returns an empty list when given a nonexistent expansion.
        """
        url = reverse("card-list-by-expansion", kwargs={"pk": self.expansion2.pk + 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])


class CardFilterByTypeTests(APITestCase):
    def setUp(self):
        self.type1 = PokemonType.objects.create(name="type 1")
        self.type2 = PokemonType.objects.create(name="type 2")
        self.card1 = Card.objects.create(
            name="card 1",
            rarity="common",
            expansion=None,
            type1=self.type1,
            type2=self.type2,
            hp=None,
            card_number=None,
            price=None,
            image=None,
        )
        self.card2 = Card.objects.create(
            name="card 2",
            rarity="rare",
            expansion=None,
            type1=self.type1,
            type2=None,
            hp=None,
            card_number=None,
            price=None,
            image=None,
        )
    def test_card_list_by_type(self):
        """
        Ensure we can retrieve cards filtered by type.
        """
        url = reverse("card-list-by-type", kwargs={"pk": self.type1.pk})
        response = self.client.get(url, format="json")
        serialized_data = CardSerializer([self.card1, self.card2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serialized_data)

    def test_card_list_by_type_invalid_pk(self):
        """
        Ensure an invalid type pk returns an empty list of results.
        """
        url = reverse("card-list-by-type", kwargs={"pk": 9999})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])


class CardFilterByRarityTestCase(APITestCase):
    def setUp(self):
        self.common_card = Card.objects.create(
            name="common card",
            rarity=Card.RarityEnum.COMMON,
            expansion=None,
            type1=None,
            type2=None,
            hp=None,
            card_number=None,
            price=None,
            image=None,
        )
        self.rare_card = Card.objects.create(
            name="rare card",
            rarity=Card.RarityEnum.RARE,
            expansion=None,
            type1=None,
            type2=None,
            hp=None,
            card_number=None,
            price=None,
            image=None,
        )
        self.uncommon_card = Card.objects.create(
            name="uncommon card",
            rarity=Card.RarityEnum.UNCOMMON,
            expansion=None,
            type1=None,
            type2=None,
            hp=None,
            card_number=None,
            price=None,
            image=None,
        )
        self.url = "/cards/rarity/"

    def test_get_cards_by_common_rarity(self):
        response = self.client.get(self.url + "common/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], self.common_card.name)

    def test_get_cards_by_rare_rarity(self):
        response = self.client.get(self.url + "rare/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], self.rare_card.name)

    def test_get_cards_by_uncommon_rarity(self):
        response = self.client.get(self.url + "uncommon/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], self.uncommon_card.name)

    def test_get_cards_by_invalid_rarity(self):
        response = self.client.get(self.url + "invalid_rarity/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)