from django.contrib import admin
from .models import Card, Expansion, PokemonType

admin.site.register(Card)
admin.site.register(Expansion)
admin.site.register(PokemonType)
