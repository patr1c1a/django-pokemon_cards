import os
import django
from django.db.utils import IntegrityError
from api.models import Card, Expansion, PokemonType

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokemon.settings")
django.setup()

card_data = [
    {
        "name": "Bulbasaur",
        "first_edition": True,
        "rarity": "common",
        "expansion": "Base Set",
        "type1": "Grass",
        "type2": "Poison",
        "hp": 40,
        "card_number": 44,
        "price": 1500.00,
        "image": "bulbasaur.jpg",
    },
    {
        "name": "Charmander",
        "first_edition": False,
        "rarity": "common",
        "expansion": "Base Set",
        "type1": "Fire",
        "type2": "",
        "hp": 50,
        "card_number": 46,
        "price": 69.94,
        "image": "charmander.jpg",
    },
    {
        "name": "Clefairy",
        "first_edition": True,
        "rarity": "rare",
        "expansion": "Base Set 2",
        "type1": "Fairy",
        "type2": "",
        "hp": 40,
        "card_number": 6,
        "price": 364,
        "image": "clefairy.jpg",
    },
    {
        "name": "Pikachu",
        "first_edition": False,
        "rarity": "rare",
        "expansion": "Base Set",
        "type1": "Electric",
        "type2": "",
        "hp": 40,
        "card_number": 58,
        "price": 89.99,
        "image": "pikachu.jpg",
    },
    {
        "name": "Metapod",
        "first_edition": True,
        "rarity": "common",
        "expansion": "Base Set",
        "type1": "Grass",
        "type2": "",
        "hp": 70,
        "card_number": 54,
        "price": 14.05,
        "image": "metapod.jpg",
    },
    {
        "name": "Lechonk",
        "first_edition": True,
        "rarity": "common",
        "expansion": "Scarlet & Violet",
        "type1": "Normal",
        "type2": "",
        "hp": 60,
        "card_number": 155,
        "price": 2.90,
        "image": "lechonk.jpg",
    },
]


def run():
    """
    Populate Pokémon cards test data into the database
    """
    try:
        for dictionary in card_data:
            card = Card(
                name=dictionary["name"],
                first_edition=dictionary["first_edition"],
                rarity=dictionary["rarity"],
                hp=dictionary["hp"],
                card_number=dictionary["card_number"],
                price=dictionary["price"],
                image=os.path.join("img", dictionary["image"]),
            )

            # Find the expansion and type references in the database (for foreign key fields)
            card.expansion = Expansion.objects.get(name=dictionary["expansion"])
            if dictionary["type1"]:
                card.type1 = PokemonType.objects.get(name=dictionary["type1"])
            if dictionary["type2"]:
                card.type2 = PokemonType.objects.get(name=dictionary["type2"])
            card.save()
        print("Cards populated successfully!")
    except IntegrityError:
        print("Some or all of the instances already exist in the database.")
    except Expansion.DoesNotExist:
        print("Expansion does not exist. Maybe you forgot to populate the Expansion table first?")
    except PokemonType.DoesNotExist:
        print("PokemonType does not exist. Maybe you forgot to populate the PokemonType table first?")
