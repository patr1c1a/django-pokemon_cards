from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

urlpatterns = [
    # cards/
    re_path(r"^cards/?$", views.CardList.as_view(), name="card-list"),

    # cards/<int:pk>/
    re_path(r"^cards/(?P<pk>\d+)/?$", views.CardDetail.as_view(), name="card-by-id"),

    # cards/expansion/<int:pk>/
    re_path(r"^cards/expansion/(?P<pk>\d+)/?$", views.CardFilterByExpansion.as_view(), name="card-list-by-expansion"),

    # cards/type/<int:pk>/
    re_path(r"^cards/type/(?P<pk>\d+)/?$", views.CardFilterByType.as_view(), name="card-list-by-type"),

    # cards/rarity/<str:rarity>/
    re_path(r"^cards/rarity/(?P<rarity>\w+)/?$", views.CardFilterByRarity.as_view(), name="card-list-by-rarity"),

    # expansions/series/<str:series_name>/
    re_path(r"^expansions/series/(?P<series_name>.+)/?$", views.ExpansionFilterBySeries.as_view(), name="expansion-list-by-series"),

    # expansions/
    re_path(r"^expansions/?$", views.ExpansionList.as_view(), name="expansion-list"),

    # expansions/<int:pk>/
    re_path(r"^expansions/(?P<pk>\d+)/?$", views.ExpansionDetail.as_view(), name="expansion-by-id"),

    # types/
    re_path(r"^types/?$", views.PokemonTypeList.as_view(), name="type-list"),

    # types/<int:pk>/
    re_path(r"^types/(?P<pk>\d+)/?$", views.PokemonTypeDetail.as_view(), name="type-by-id"),

    # types/name/<str:type_name>/
    re_path(r"^types/name/(?P<type_name>.+)/?$", views.PokemonTypeFilterByName.as_view(), name="type-filter-by-name")
]

urlpatterns = format_suffix_patterns(urlpatterns)
