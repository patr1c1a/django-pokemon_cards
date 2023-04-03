import os
import django
from sqlite3 import IntegrityError
from api.models import PokemonType

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pokemon.settings")
django.setup()

type_data = [
    {
        "name": "Normal",
        "strong_vs": "",
        "weak_vs": "Rock, Steel, Ghost",
        "resists": "Ghost",
        "vulnerable_to": "Fighting",
    },
    {
        "name": "Fighting",
        "strong_vs": "Normal, Rock, Steel, Ice, Dark",
        "weak_vs": "Flying, Poison, Bug, Psychic, Ghost",
        "resists": "Rock, Bug, Dark",
        "vulnerable_to": "Flying, Psychic, Fairy",
    },
    {
        "name": "Flying",
        "strong_vs": "Fighting, Bug, Grass, Fairy",
        "weak_vs": "Rock, Steel, Electric",
        "resists": "Ground, Fighting, Bug, Grass",
        "vulnerable_to": "Rock, Electric, Ice",
    },
    {
        "name": "Poison",
        "strong_vs": "Grass, Fairy",
        "weak_vs": "Poison, Ground, Rock, Ghost",
        "resists": "Fighting, Poison, Bug, Grass, Fairy",
        "vulnerable_to": "Ground, Psychic",
    },
    {
        "name": "Ground",
        "strong_vs": "Poison, Rock, Steel, Fire, Electric",
        "weak_vs": "Bug, Grass",
        "resists": "Poison, Rock",
        "vulnerable_to": "Water, Grass, Ice",
    },
    {
        "name": "Rock",
        "strong_vs": "Flying, Bug, Fire, Ice",
        "weak_vs": "Fighting, Ground, Steel",
        "resists": "Poison, Rock",
        "vulnerable_to": "Water, Grass, Ice",
    },
    {
        "name": "Bug",
        "strong_vs": "Grass, Psychic, Dark",
        "weak_vs": "Fighting, Flying, Poison, Ghost, Steel, Fire, Fairy",
        "resists": "Fighting, Ground, Grass",
        "vulnerable_to": "Flying, Rock, Fire",
    },
    {
        "name": "Ghost",
        "strong_vs": "Ghost, Psychic",
        "weak_vs": "Dark",
        "resists": "Normal, Fighting, Poison, Bug",
        "vulnerable_to": "Ghost, Dark",
    },
    {
        "name": "Steel",
        "strong_vs": "Rock, Ice, Fairy",
        "weak_vs": "Steel, Fire, Water, Electric",
        "resists": "Normal, Flying, Poison, Rock, Bug, Steel, Grass, Psychic, Ice, Dragon, Fairy",
        "vulnerable_to": "Fighting, Fire, Poison",
    },
    {
        "name": "Fire",
        "strong_vs": "Bug, Steel, Grass, Ice",
        "weak_vs": "Rock, Fire, Water, Dragon",
        "resists": "Bug, Steel, Fire, Grass, Ice, Fairy",
        "vulnerable_to": "Ground, Rock, Water",
    },
    {
        "name": "Water",
        "strong_vs": "Ground, Rock, Fire",
        "weak_vs": "Water, Grass, Dragon",
        "resists": "Steel, Fire, Water, Ice",
        "vulnerable_to": "Grass, Electric",
    },
    {
        "name": "Grass",
        "strong_vs": "Ground, Rock, Water",
        "weak_vs": "Flying, Poison, Bug, Steel, Fire, Grass",
        "resists": "Water, Grass, Electric",
        "vulnerable_to": "Flying, Poison, Bug, Fire, Ice",
    },
    {
        "name": "Electric",
        "strong_vs": "Flying, Water",
        "weak_vs": "Ground, Grass, Electric",
        "resists": "Flying, Steel, Electric",
        "vulnerable_to": "Ground",
    },
    {
        "name": "Psychic",
        "strong_vs": "Fighting, Poison",
        "weak_vs": "Steel, Psychic, Dark",
        "resists": "Fighting, Psychic",
        "vulnerable_to": "Bug, Ghost, Dark",
    },
    {
        "name": "Ice",
        "strong_vs": "Flying, Ground, Grass, Dragon",
        "weak_vs": "Steel, Fire, Water, Ice",
        "resists": "Ice",
        "vulnerable_to": "Fighting, Rock, Steel, Fire",
    },
    {
        "name": "Dragon",
        "strong_vs": "Dragon",
        "weak_vs": "Steel",
        "resists": "Fire, Water, Grass, Electric",
        "vulnerable_to": "Ice, Dragon, Fairy",
    },
    {
        "name": "Dark",
        "strong_vs": "Ghost, Psychic",
        "weak_vs": "Fighting, Dark, Fairy",
        "resists": "Ghost, Psychic, Dark",
        "vulnerable_to": "Fighting, Bug, Fairy",
    },
    {
        "name": "Fairy",
        "strong_vs": "Fighting, Dragon, Dark",
        "weak_vs": "Poison, Steel, Fire",
        "resists": "Fighting, Bug, Dark",
        "vulnerable_to": "Poison, Ghost, Dragon",
    },
]


def run():
    """
    Populate Pokémon types test data into the database
    """
    # Create types with just their name
    try:
        types = [PokemonType(name=dictionary["name"]) for dictionary in type_data]
        PokemonType.objects.bulk_create(types)
        print("Type names populated successfully! Now updating records to add more information...")
    except IntegrityError:
        print("Some or all of the instances already exist in the database.")

    # Update records to create relationships with other types
    try:
        for dictionary in type_data:
            selected_type = PokemonType.objects.get(
                name=dictionary["name"]
            )  # finds the PokemonType to be updated

            # Updates "strong_vs" field
            if dictionary["strong_vs"]:
                strong_vs_as_str = list(
                    dictionary["strong_vs"].split(", ")
                )  # list of strong_vs names for the selected type
                strong_vs_as_objects = [
                    PokemonType.objects.get(name=type_name)
                    for type_name in strong_vs_as_str
                ]
                selected_type.strong_vs.add(*strong_vs_as_objects)

            # Updates "resistant_to" field
            if dictionary["resists"]:
                resistant_to_as_str = list(
                    dictionary["resists"].split(", ")
                )  # list of resistant_to names for the selected type
                resistant_to_as_objects = [
                    PokemonType.objects.get(name=type_name)
                    for type_name in resistant_to_as_str
                ]
                selected_type.resistant_to.add(*resistant_to_as_objects)

            # Updates "vulnerable_to" field
            if dictionary["vulnerable_to"]:
                vulnerable_to_as_str = list(
                    dictionary["vulnerable_to"].split(", ")
                )  # list of vulnerable_to names for the selected type
                vulnerable_to_as_objects = [
                    PokemonType.objects.get(name=type_name)
                    for type_name in vulnerable_to_as_str
                ]
                selected_type.vulnerable_to.add(*vulnerable_to_as_objects)

            # Updates "weak_vs" field
            if dictionary["weak_vs"]:
                weak_vs_as_str = list(
                    dictionary["weak_vs"].split(", ")
                )  # list of weak_vs names for the selected type
                weak_vs_as_objects = [
                    PokemonType.objects.get(name=type_name)
                    for type_name in weak_vs_as_str
                ]
                selected_type.weak_vs.add(*weak_vs_as_objects)
        print("Records updated successfully!")
    except PokemonType.DoesNotExist:
        print("PokemonType does not exist.")
