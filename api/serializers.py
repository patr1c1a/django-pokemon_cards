from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from api.models import Card, Expansion, PokemonType


class ExpansionSerializer(serializers.ModelSerializer):
    """
    A serializer for the Expansion model that includes all fields.
    """
    class Meta:
        model = Expansion
        fields = "__all__"

    def validate_name(self, data):
        """
        Checks that the name field is not a number.
        """
        try:
            float(data)
            raise serializers.ValidationError("Name must not be a number.")
        except ValueError:
            pass
        return data

    def validate_series(self, data):
        """
        Checks that the series field is not a number.
        """
        try:
            float(data)
            raise serializers.ValidationError("Series must not be a number.")
        except ValueError:
            pass
        return data

    def validate_release_date(self, data):
        """
        Verifies that `release_date` is not in the future.
        """
        if data and data > timezone.now().date():
            raise serializers.ValidationError("Release date cannot be in the future.")
        return data

    def create(self, validated_data):
        """
        Catches IntegrityError exceptions when creating an Expansion.
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "Expansion with this name and series already exists."
            )

    def update(self, instance, validated_data):
        """
        Catches IntegrityError exceptions when updating Expansions.
        """
        try:
            return super().update(instance, validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "Expansion with this name already exists."
            )


class PokemonTypeSerializer(serializers.ModelSerializer):
    """
    A serializer for the PokemonType model that includes all fields.
    This serializer uses the `SimplePokemonTypeSerializer` to serialize the
    `ManyToManyField`s without causing a recursive loop.
    """
    class Meta:
        model = PokemonType
        fields = "__all__"

    def validate_name(self, data):
        """
        Checks that the name field is not a number.
        """
        try:
            float(data)
            raise serializers.ValidationError("Name must not be a number.")
        except ValueError:
            pass
        return data

    def to_representation(self, instance):
        """
        Overrides the `to_representation` method to display the whole objects for the
        `strong_vs`, `weak_vs`, `resistant_to` and `vulnerable_to` fields instead of
        just the primary keys.
        Maps the field names to their serialized values or None if the related object
        does not exist, to avoid showing empty objects when any of these optional fields
        are not present in the PokemonType.
        """
        representation = super().to_representation(instance)
        related_fields = ["strong_vs", "weak_vs", "resistant_to", "vulnerable_to"]
        related_data = {}
        for field in related_fields:
            related_data[field] = list(getattr(instance, field).values_list("name", flat=True))
        representation.update(related_data)
        return representation

    def create(self, validated_data):
        """
        Catches IntegrityError exceptions when creating a PokemonType.
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "Pokemon type with this name already exists."
            )

    def update(self, instance, validated_data):
        """
        Catches IntegrityError exceptions when updating PokemonTypes.
        """
        try:
            return super().update(instance, validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "Pokemon type with this name already exists."
            )


class CardSerializer(serializers.ModelSerializer):
    """
    A serializer for the Card model that includes all fields.
    """
    expansion = serializers.PrimaryKeyRelatedField(
        queryset=Expansion.objects.all(), required=False, allow_null=True
    )
    type1 = serializers.PrimaryKeyRelatedField(
        queryset=PokemonType.objects.all(), required=False, allow_null=True
    )
    type2 = serializers.PrimaryKeyRelatedField(
        queryset=PokemonType.objects.all(), required=False, allow_null=True
    )
    rarity = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Card
        fields = ("id", "name", "rarity", "hp", "type1", "type2", "expansion", "card_number", "first_edition", "price",
                  "image", "created")

    def validate_name(self, data):
        """
        Checks that the name field is not a number.
        """
        try:
            float(data)
            raise serializers.ValidationError("Name must not be a number.")
        except ValueError:
            pass
        return data

    def validate_hp(self, data):
        """
        Validates `hp` is a multiple of 10.
        """
        if data % 10 != 0:
            raise ValidationError("HP must be a multiple of 10.")
        return data

    def validate_rarity(self, data):
        if data.lower() not in Card.RarityEnum.values:
            raise serializers.ValidationError(f"{data} is not a valid rarity.")
        return data.lower()

    def to_representation(self, instance):
        """
        Overrides the `to_representation` method to display the whole object for the
        `expansion`, `type1`, and `type2` fields instead of just the primary key.
        Maps the field names to their serialized values or None if the related object
        does not exist, to avoid showing empty objects when any of these optional fields
        are not present in the Card.
        """
        representation = super().to_representation(instance)
        related_fields = {
            "expansion": ExpansionSerializer,
            "type1": PokemonTypeSerializer,
            "type2": PokemonTypeSerializer,
        }
        related_data = {
            field: serializer(getattr(instance, field)).data
            if getattr(instance, field)
            else None
            for field, serializer in related_fields.items()
        }
        representation.update(related_data)
        return representation

    def create(self, validated_data):
        """
        Catches IntegrityError exceptions when creating a Card.
        """
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError("Card with this name already exists.")

    def update(self, instance, validated_data):
        """
        Catches IntegrityError exceptions when updating a Card.
        """
        try:
            return super().update(instance, validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                "Expansion with this name and series already exists."
            )
