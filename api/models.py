from django.db import models
from django_enum import EnumField
from django.db.models.functions import Lower


class Expansion(models.Model):
	"""
	Pokémon expansion
	"""
	class Meta:
		constraints = [
			models.UniqueConstraint(
				Lower('name'), Lower('series'), name='unique_expansion_name_series'
			)
		]
		ordering = ['id']

	name = models.CharField(max_length=100, blank=False)
	series = models.CharField(max_length=100, blank=False)
	cards = models.IntegerField(blank=True, null=True)
	release_date = models.DateField(blank=True, null=True)
	promotional_set = models.BooleanField(blank=True, null=True)

	def __str__(self):
		return f"{self.name} (ID: {self.pk}). SERIES: {self.series}. No. OF CARDS: {self.cards}. RELEASED: " \
			   f"{self.release_date}. PROMOTIONAL SET?: {self.promotional_set}."

	def __repr__(self):
		return object.__repr__(self) + f"ID: {self.pk}. EXPANSION NAME: {self.name!r}. SERIES: {self.series}. " \
									   f"No. OF CARDS: {self.cards}. RELEASED: {self.release_date}. " \
									   f"PROMOTIONAL SET?: {self.promotional_set}."


class PokemonType(models.Model):
	"""
	Pokémon type
	"""
	class Meta:
		constraints = [
			models.UniqueConstraint(Lower('name'), name='unique_type_name')
		]
		ordering = ['id']

	name = models.CharField(max_length=100, blank=False)
	strong_vs = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="strong_versus")
	weak_vs = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="weak_versus")
	resistant_to = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="resists")
	vulnerable_to = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="vulnerable")
	
	def __str__(self):
		strong_vs_names =  ", ".join(self.strong_vs.values_list('name', flat=True))
		weak_vs_names =  ", ".join(self.weak_vs.values_list('name', flat=True))
		resistant_to_names =  ", ".join(self.resistant_to.values_list('name', flat=True))
		vulnerable_to_names = ", ".join(self.vulnerable_to.values_list('name', flat=True))
		return f"{self.name} (ID: {self.pk}). STRONG VS: {strong_vs_names}. WEAK VS: {weak_vs_names}. RESISTS: " \
			   f"{resistant_to_names}. VULNERABLE TO: {vulnerable_to_names}."

	def __repr__(self):
		return object.__repr__(self) + f"ID: {self.pk}. NAME: {self.name!r}. STRONG VS: " \
									   f"{self.strong_vs.values_list('name', flat=True)}. " \
									   f"WEAK VS: {self.weak_vs.values_list('name', flat=True)}. " \
									   f"RESISTS: {self.resistant_to.values_list('name', flat=True)}. " \
									   f"VULNERABLE TO: {self.vulnerable_to.values_list('name', flat=True)} ). "


class Card(models.Model):
	"""
	Pokémon card.
	"""
	class RarityEnum(models.TextChoices):
		"""
		Choices for Card rarity
		"""
		COMMON = 'common'
		UNCOMMON = 'uncommon'
		RARE = 'rare'

	class Meta:
		constraints = [
			models.UniqueConstraint(Lower('name'), name='unique_card_name')
		]
		ordering = ['id']

	name = models.CharField(max_length=100, blank=False)
	first_edition = models.BooleanField(blank=True, null=True)
	rarity = EnumField(RarityEnum, blank=True, null=True)
	expansion = models.ForeignKey(Expansion, on_delete=models.PROTECT, blank=True, null=True, related_name="expansion", default=None)
	type1 = models.ForeignKey(PokemonType, on_delete=models.PROTECT, blank=True, null=True, related_name="type1", default=None)
	type2 = models.ForeignKey(PokemonType, on_delete=models.PROTECT, blank=True, null=True, related_name="type2", default=None)
	hp = models.PositiveIntegerField(blank=True, null=True)
	card_number = models.PositiveIntegerField(blank=True, null=True)
	price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
	image = models.ImageField(upload_to="img", blank=True, null=True)
	created = models.DateField(auto_now_add=True)

	def __str__(self):
		return f"NAME: {self.name}. HP: {self.hp}. TYPE 1: {self.type1}. TYPE 2: {self.type2}. RARITY: {self.rarity}," \
			   f"EXPANSION: {self.expansion}. PRICE: {self.price}. CARD No.: {self.card_number}. CREATION DATE: " \
			   f"{self.created}. FIRST EDITION?: {self.first_edition}. IMAGE: {self.image}."

	def __repr__(self):
		return object.__repr__(self) + f"ID: {self.pk}. NAME: {self.name!r}. HP: {self.hp}. TYPE1: {self.type1}. " \
									   f"TYPE2: {self.type2}. RARITY: {self.rarity}. EXPANSION: {self.expansion}. " \
									   f"PRICE: {self.price}. CREATED: {self.created}. CARD_NUMBER: {self.card_number} " \
									   f"FIRST_EDITION: {self.first_edition}. IMAGE: {self.image}."
