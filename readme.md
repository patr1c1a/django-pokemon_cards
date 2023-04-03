Pokémon Cards API with Django Rest Framework 
==================

Django-based RESTful API for managing Pokémon Cards.



Getting Started
---------------

These instructions will get you a copy of the project up and running on your local machine for development and testing 
purposes.

### Prerequisites

-   Python 3.x
-   pip
-   virtualenv (optional)

### Installing

1.  Clone the repository
2.  Create and activate a virtual environment (optional)
3.  Install the dependencies:

`pip install -r requirements.txt`

4.  Create a Django secret key and paste it in `pokemon/secrets.py`, replacing `your_secret_key_here` with it: 

`python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`


5.  Create a sqlite3 database superuser, choosing a username and password (you'll need these credentials to 
authenticate in order to use the API):

`python manage.py createsuperuser`

6.  Optionally, you can populate some or all of the tables in the database with some example data (the images included 
in `/media/img` are related to these, and you can safely delete them if not needed):

`python manage.py runscript populate_expansions`

`python manage.py runscript populate_types`

`python manage.py runscript populate_cards`

7. Run the server:

`python manage.py runserver 8000`

The API should now be accessible at <http://localhost:8000>.



Resources
--------

### Card (endpoint: /card/)

* `id`: Autonumeric field that represents the primary key in the database. Read-only field.
* `name`: Card name (e.g.: "Pikachu"). Required field.
* `rarity`: Enum field with 3 possible values: "common", "uncommon", "rare". Optional field.
* `hp`: Pokémon HP value. Must be a multiple of 10. Optional field.
* `type1`: Main Pokémon type (e.g.: "fire"). A foreign key to the *PokemonType* model. Optional field. 
* `type2`: Secondary Pokémon type (e.g.: "water"). A foreign key to the *PokemonType* model. Optional field.
* `expansion`: The expansion a card belongs to. A foreign key to the *Expansion* model. Optional field.
* `card_number`: Card number in the expansion. Optional field.
* `first_edition`: Boolean that represents whether the card is a first edition or not. Optional field.
* `price`: Card price. Optional field.
* `image`: An image of the card. These are uploaded to the *<project_root>/media/img* folder. Optional field.
* `created`: Date of card creation. Automatically defaults to the current date of entry. Read-only field.

### Expansion (endpoint: /expansion/)

* `id`: Autonumeric field that represents the primary key in the database. Read-only field.
* `name`: Expansion name (e.g.: "Base Set"). Required field.
* `series`: Name of the series the expansion belongs to (e.g: "Original Series"). Optional field.
* `cards`: Number of cards in the expansion. Optional field.
* `release_date`: Release date of the expansion, in YYYY-MM-DD format. Optional field.
* `promotional_set`: Boolean that represents whether the expansion is a promotional set or not. Optional field.

### PokemonType (endpoint: /type/)

* `id`: Autonumeric field that represents the primary key in the database. Read-only field.
* `name`: A Pokémon type (e.g.: "Fire"). Required field.
* `strong_vs`: A list of other Pokémon types the current type is strong against. A list of foreign keys to the
*PokemonType* model. Optional field.
* `weak_vs`: A list of other Pokémon types the current type is weak against. A list of foreign keys to the *PokemonType*
model. Optional field.
* `resistant_to`: A list of other Pokémon types the current type is resistant to. A list of foreign keys to the 
*PokemonType* model. Optional field. 
* `vulnerable_to`:  A list of other Pokémon types the current type is vulnerable to. A list of foreign keys to the 
*PokemonType* model. Optional field. 



Access the API
--------------

### Browser

Once the server is running, a basic UI for this API will be available through http://localhost:8000/admin/



### REST Client (e.g.: Postman)

Authentication should be done using the username and password created in step 4 of installation instructions.

If a "CSRF verification failed. Request aborted" error occurs, then a CSRF token is needed. To get it, make a GET 
request to any of the endpoints and find the `csrftoken` cookie returned with the response. Then include the cookie 
value in a `X-CSRFToken` header on any request that needs it (if using Postman, this would go in the "Headers" section,
with a `X-CSRFToken:<token value here>` key/value pair).



Endpoints
---------

Swagger documentation is available at http://localhost:8000/api/schema/swagger-ui/ (project must be running) and a 
downloadable yaml file is available at http://localhost:8000/api/schema/.

### Overview

Pagination is enabled (defaults to 10 items per page).

* `/cards/`: GET, POST. Filters: **search** parameter allows searching in the *name* and *rarity* fields (e.g.: 
http://localhost:8000/cards/?search=common); **created** parameter allows filtering by day, month or year in the
release_date field (e.g: http://localhost:8000/cards/?created__year=2023).

* `/cards/{id}/`: GET, PUT, PATCH, DELETE

* `/cards/expansion/{id}/`: GET

* `/cards/rarity/{rarity}/`: GET

* `/cards/type/{id}/`: GET

* `/expansions/`: GET, POST. Filters: **search** parameter allows searching in the *name* and *series* fields (e.g.: 
http://localhost:8000/expansions/?search=original%20series); **release_date** parameter allows filtering by day, month or year in the
release_date field (e.g: http://localhost:8000/expansions/?release_date__year=2000).

* `/expansions/{id}/`: GET, PUT, PATCH, DELETE

* `/expansions/series/{series_name}/` GET

* `/types/` GET, POST. Filters: **search** parameter allows searching in the *name* field (e.g.: 
http://localhost:8000/types?search=electric).

* `/types/{id}/` GET, PUT, PATCH, DELETE

* `/types/name/{type_name}/`: GET



Running unit tests
-----------------

To run all tests, execute:

`python manage.py test api.tests`

To run a specific test file:

`python manage.py test api.tests.models.<category>.<file>`

You should replace `<category>` with the name of directory containing the file (`model`, `view` or `serializer`) and 
<file> with the file name:
* `test_card_<category>`
* `test_pokemontype_<category>`
* `test_expansion_<category>`

E.g.: *test_card_model*, *test_card_serializer*, *test_card_view*.



Migrations
----------

Should you make any changes to the model, migrations might be needed to update the database:

`python manage.py makemigrations`

`python manage.py migrate`



License
----------

This project is licensed under the MIT License - see the LICENSE file for details.