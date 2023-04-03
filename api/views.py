from rest_framework import generics
from rest_framework.exceptions import ValidationError
from api.models import Expansion, PokemonType, Card
from api.serializers import ExpansionSerializer, PokemonTypeSerializer, CardSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "results": data,
            }
        )


class ExpansionList(generics.ListCreateAPIView):
    queryset = Expansion.objects.all()
    serializer_class = ExpansionSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name", "series"]
    filterset_fields = {"release_date": ["year", "month", "day"]}


class ExpansionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expansion.objects.all()
    serializer_class = ExpansionSerializer


class ExpansionFilterBySeries(generics.ListAPIView):
    serializer_class = ExpansionSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Optionally restricts the returned expansions to a given series,
        by filtering against a `series` (str) query parameter in the URL.
        """
        queryset = Expansion.objects.all()
        given_series = self.kwargs.get("series_name", "None")
        if given_series:
            queryset = queryset.filter(series__iexact=given_series)
        return queryset


class PokemonTypeList(generics.ListCreateAPIView):
    queryset = PokemonType.objects.all()
    serializer_class = PokemonTypeSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class PokemonTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PokemonType.objects.all()
    serializer_class = PokemonTypeSerializer


class PokemonTypeFilterByName(generics.ListAPIView):
    serializer_class = PokemonTypeSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Optionally restricts the returned types to a given name,
        by filtering against a `name` (str) query parameter in the URL.
        """
        queryset = PokemonType.objects.all()
        given_name = self.kwargs.get("type_name", "None")
        if given_name:
            queryset = queryset.filter(name__iexact=given_name)
        return queryset


class CardList(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ["name", "rarity"]
    filterset_fields = {"created": ["year", "month", "day"]}


class CardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardFilterByExpansion(generics.ListAPIView):
    serializer_class = CardSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Optionally restricts the returned cards to a given expansion,
        by filtering against an `expansion` (id) query parameter in the URL.
        """
        queryset = Card.objects.all()
        expansion_pk = self.kwargs.get("pk", "None")
        if expansion_pk:
            queryset = queryset.filter(expansion=expansion_pk)
        return queryset


class CardFilterByType(generics.ListAPIView):
    serializer_class = CardSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Optionally restricts the returned cards to a given type1 or type2,
        by filtering against a `type` (id) query parameter in the URL.
        Only one type is given in the URL and any card matching it either as
        type1 or type2, will be retrieved.
        """
        queryset = Card.objects.all()
        type_pk = self.kwargs.get("pk")
        if type_pk:
            queryset = queryset.filter(type1=type_pk) | queryset.filter(type2=type_pk)
        return queryset


class CardFilterByRarity(generics.ListAPIView):
    serializer_class = CardSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Optionally restricts the returned cards to a given rarity,
        by filtering against a `rarity` query parameter in the URL.
        """
        given_rarity = self.kwargs.get("rarity", "None").upper()
        try:
            rarity_enum_member = Card.RarityEnum[given_rarity]
        except KeyError:
            raise ValidationError("Invalid rarity value")
        return Card.objects.filter(rarity=rarity_enum_member)
