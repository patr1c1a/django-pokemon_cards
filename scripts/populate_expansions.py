import os
import django
from sqlite3 import IntegrityError
from api.models import Expansion

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokemon.settings')
django.setup()

expansion_data = [
	{
		"series": "Original Series",
		"name": "Base Set",
		"cards": 102,
		"release_date": "1999-01-09",
		"promotional_set": False
	},
	{
		"series": "Original Series",
		"name": "Jungle",
		"cards": 64,
		"release_date": "1999-06-16",
		"promotional_set": False
	},
	{
		"series": "Original Series",
		"name": "Fossil",
		"cards": 62,
		"release_date": "1999-10-10",
		"promotional_set": False
	},
	{
		"series": "Original Series",
		"name": "Base Set 2",
		"cards": 130,
		"release_date": "2000-02-24",
		"promotional_set": False
	},
	{
		"series": "Original Series",
		"name": "Team Rocket",
		"cards": 83,
		"release_date": "2000-04-24",
		"promotional_set": False
	},
	{
		"series": "Original Series",
		"name": "Gym Heroes",
		"cards": 132,
		"release_date": "2000-08-14",
		"promotional_set": False
	},
	{
		"series": "Original Series",
		"name": "Gym Challenge",
		"cards": 132,
		"release_date": "2000-10-16",
		"promotional_set": False
	},
	{
		"series": "Neo Series",
		"name": "Neo Genesis",
		"cards": 111,
		"release_date": "2000-12-16",
		"promotional_set": False
	},
	{
		"series": "Neo Series",
		"name": "Neo Discovery",
		"cards": 75,
		"release_date": "2001-06-01",
		"promotional_set": False
	},
	{
		"series": "Neo Series",
		"name": "Neo Revelation",
		"cards": 66,
		"release_date": "2001-09-21",
		"promotional_set": False
	},
	{
		"series": "Neo Series",
		"name": "Neo Destiny",
		"cards": 113,
		"release_date": "2002-02-28",
		"promotional_set": False
	},
	{
		"series": "Legendary Collection Series",
		"name": "Legendary Collection",
		"cards": 110,
		"release_date": "2002-05-24",
		"promotional_set": False
	},
	{
		"series": "e-Card Series",
		"name": "Expedition Base Set",
		"cards": 165,
		"release_date": "2002-09-15",
		"promotional_set": False
	},
	{
		"series": "e-Card Series",
		"name": "Aquapolis",
		"cards": 182,
		"release_date": "2003-01-15",
		"promotional_set": False
	},
	{
		"series": "e-Card Series",
		"name": "Skyridge",
		"cards": 182,
		"release_date": "2003-05-12",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Ruby & Sapphire",
		"cards": 109,
		"release_date": "2003-07-01",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Sandstorm",
		"cards": 100,
		"release_date": "2003-09-18",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Dragon",
		"cards": 100,
		"release_date": "2003-09-18",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Team Magma vs Team Aqua",
		"cards": 97,
		"release_date": "2004-03-01",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Hidden Legends",
		"cards": 102,
		"release_date": "2004-06-01",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX FireRed & LeafGreen",
		"cards": 114,
		"release_date": "2004-09-01",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Team Rocket Returns",
		"cards": 111,
		"release_date": "2004-11-01",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Deoxys",
		"cards": 108,
		"release_date": "2005-02-01",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Emerald",
		"cards": 107,
		"release_date": "2005-05-01",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Unseen Forces",
		"cards": 145,
		"release_date": "2005-08-01",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Delta Species",
		"cards": 114,
		"release_date": "2005-10-31",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Legend Maker",
		"cards": 93,
		"release_date": "2006-02-01",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Holon Phantoms",
		"cards": 111,
		"release_date": "2006-05-01",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Crystal Guardians",
		"cards": 100,
		"release_date": "2006-08-01",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Dragon Frontiers",
		"cards": 101,
		"release_date": "2006-11-01",
		"promotional_set": False
	},
	{
		"series": "EX Series",
		"name": "EX Power Keepers",
		"cards": 108,
		"release_date": "2007-02-01",
		"promotional_set": False
	},
	{
		"series": "Diamond & Pearl Series",
		"name": "Diamond & Pearl",
		"cards": 130,
		"release_date": "2007-05-23",
		"promotional_set": False
	},
	{
		"series": "Diamond & Pearl Series",
		"name": "Mysterious Treasures",
		"cards": 124,
		"release_date": "2007-08-22",
		"promotional_set": False
	},
	{
		"series": "Diamond & Pearl Series",
		"name": "Secret Wonders",
		"cards": 132,
		"release_date": "2007-11-07",
		"promotional_set": False
	},
	{
		"series": "Diamond & Pearl Series",
		"name": "Great Encounters",
		"cards": 106,
		"release_date": "2008-02-13",
		"promotional_set": False
	},
	{
		"series": "Diamond & Pearl Series",
		"name": "Majestic Dawn",
		"cards": 100,
		"release_date": "2008-05-21",
		"promotional_set": False
	},
	{
		"series": "Diamond & Pearl Series",
		"name": "Legends Awakened",
		"cards": 146,
		"release_date": "2008-08-20",
		"promotional_set": False
	},
	{
		"series": "Diamond & Pearl Series",
		"name": "Stormfront",
		"cards": 106,
		"release_date": "2008-11-05",
		"promotional_set": False
	},
	{
		"series": "Platinum Series",
		"name": "Platinum",
		"cards": 133,
		"release_date": "2009-02-11",
		"promotional_set": False
	},
	{
		"series": "Platinum Series",
		"name": "Rising Rivals",
		"cards": 120,
		"release_date": "2009-05-16",
		"promotional_set": False
	},
	{
		"series": "Platinum Series",
		"name": "Supreme Victors",
		"cards": 153,
		"release_date": "2009-08-19",
		"promotional_set": False
	},
	{
		"series": "Platinum Series",
		"name": "Arceus",
		"cards": 111,
		"release_date": "2009-11-04",
		"promotional_set": False
	},
	{
		"series": "HeartGold & SoulSilver Series",
		"name": "HeartGold & SoulSilver",
		"cards": 124,
		"release_date": "2010-02-10",
		"promotional_set": False
	},
	{
		"series": "HeartGold & SoulSilver Series",
		"name": "Unleashed",
		"cards": 96,
		"release_date": "2010-05-12",
		"promotional_set": False
	},
	{
		"series": "HeartGold & SoulSilver Series",
		"name": "Undaunted",
		"cards": 91,
		"release_date": "2010-08-18",
		"promotional_set": False
	},
	{
		"series": "HeartGold & SoulSilver Series",
		"name": "Triumphant",
		"cards": 103,
		"release_date": "2010-11-03",
		"promotional_set": False
	},
	{
		"series": "Call of Legends Series",
		"name": "Call of Legends",
		"cards": 106,
		"release_date": "2011-02-09",
		"promotional_set": False
	},
	{
		"series": "Black & White Series",
		"name": "Black & White",
		"cards": 115,
		"release_date": "2011-04-25",
		"promotional_set": False
	},
	{
		"series": "Black & White Series",
		"name": "Emerging Powers",
		"cards": 98,
		"release_date": "2011-08-31",
		"promotional_set": False
	},
	{
		"series": "Black & White Series",
		"name": "Noble Victories",
		"cards": 102,
		"release_date": "2011-11-16",
		"promotional_set": False
	},
	{
		"series": "Black & White Series",
		"name": "Next Destinies",
		"cards": 103,
		"release_date": "2012-02-08",
		"promotional_set": False
	},
	{
		"series": "Black & White Series",
		"name": "Dark Explorers",
		"cards": 111,
		"release_date": "2012-05-09",
		"promotional_set": False
	},
	{
		"series": "Black & White Series",
		"name": "Dragons Exalted",
		"cards": 128,
		"release_date": "2012-08-15",
		"promotional_set": False
	},
	{
		"series": "Black & White Series",
		"name": "Boundaries Crossed",
		"cards": 153,
		"release_date": "2012-11-07",
		"promotional_set": False
	},
	{
		"series": "Black & White Series",
		"name": "Plasma Storm",
		"cards": 138,
		"release_date": "2013-02-06",
		"promotional_set": False
	},
	{
		"series": "Black & White Series",
		"name": "Plasma Freeze",
		"cards": 122,
		"release_date": "2013-05-08",
		"promotional_set": False
	},
	{
		"series": "Black & White Series",
		"name": "Plasma Blast",
		"cards": 105,
		"release_date": "2013-08-14",
		"promotional_set": False
	},
	{
		"series": "Black & White Series",
		"name": "Legendary Treasures",
		"cards": 140,
		"release_date": "2013-11-06",
		"promotional_set": False
	},
	{
		"series": "XY Series",
		"name": "Kalos Starter Set",
		"cards": 39,
		"release_date": "2013-11-08",
		"promotional_set": False
	},
	{
		"series": "XY Series",
		"name": "XY",
		"cards": 146,
		"release_date": "2014-02-05",
		"promotional_set": False
	},
	{
		"series": "XY Series",
		"name": "Flashfire",
		"cards": 109,
		"release_date": "2014-05-07",
		"promotional_set": False
	},
	{
		"series": "XY Series",
		"name": "Furious Fists",
		"cards": 113,
		"release_date": "2014-08-13",
		"promotional_set": False
	},
	{
		"series": "XY Series",
		"name": "Phantom Forces",
		"cards": 122,
		"release_date": "2014-11-05",
		"promotional_set": False
	},
	{
		"series": "XY Series",
		"name": "Primal Clash",
		"cards": 164,
		"release_date": "2015-02-04",
		"promotional_set": False
	},
	{
		"series": "XY Series",
		"name": "Roaring Skies",
		"cards": 110,
		"release_date": "2015-05-06",
		"promotional_set": False
	},
	{
		"series": "XY Series",
		"name": "Ancient Origins",
		"cards": 100,
		"release_date": "2015-08-12",
		"promotional_set": False
	},
	{
		"series": "XY BREAK Series",
		"name": "BREAKthrough",
		"cards": 164,
		"release_date": "2015-11-04",
		"promotional_set": False
	},
	{
		"series": "XY BREAK Series",
		"name": "BREAKpoint",
		"cards": 123,
		"release_date": "2016-02-03",
		"promotional_set": False
	},
	{
		"series": "XY BREAK Series",
		"name": "Fates Collide",
		"cards": 125,
		"release_date": "2016-05-02",
		"promotional_set": False
	},
	{
		"series": "XY BREAK Series",
		"name": "Steam Siege",
		"cards": 116,
		"release_date": "2016-08-03",
		"promotional_set": False
	},
	{
		"series": "XY BREAK Series",
		"name": "Evolutions",
		"cards": 113,
		"release_date": "2016-11-02",
		"promotional_set": False
	},
	{
		"series": "Sun & Moon Series",
		"name": "Sun & Moon",
		"cards": 163,
		"release_date": "2017-02-03",
		"promotional_set": False
	},
	{
		"series": "Sun & Moon Series",
		"name": "Guardians Rising",
		"cards": 169,
		"release_date": "2017-05-05",
		"promotional_set": False
	},
	{
		"series": "Sun & Moon Series",
		"name": "Burning Shadows",
		"cards": 169,
		"release_date": "2017-08-04",
		"promotional_set": False
	},
	{
		"series": "Sun & Moon Series",
		"name": "Crimson Invasion",
		"cards": 124,
		"release_date": "2017-11-03",
		"promotional_set": False
	},
	{
		"series": "Sun & Moon Series",
		"name": "Ultra Prism",
		"cards": 173,
		"release_date": "2018-02-02",
		"promotional_set": False
	},
	{
		"series": "Sun & Moon Series",
		"name": "Forbidden Light",
		"cards": 146,
		"release_date": "2018-05-04",
		"promotional_set": False
	},
	{
		"series": "Sun & Moon Series",
		"name": "Celestial Storm",
		"cards": 183,
		"release_date": "2018-08-03",
		"promotional_set": False
	},
	{
		"series": "Sun & Moon Series",
		"name": "Lost Thunder",
		"cards": 236,
		"release_date": "2018-11-02",
		"promotional_set": False
	},
	{
		"series": "Sun & Moon Series",
		"name": "Team Up",
		"cards": 196,
		"release_date": "2019-02-01",
		"promotional_set": False
	},
	{
		"series": "Sun & Moon Series",
		"name": "Unbroken Bonds",
		"cards": 234,
		"release_date": "2019-05-03",
		"promotional_set": False
	},
	{
		"series": "Sun & Moon Series",
		"name": "Unified Minds",
		"cards": 256,
		"release_date": "2019-08-02",
		"promotional_set": False
	},
	{
		"series": "Sun & Moon Series",
		"name": "Cosmic Eclipse",
		"cards": 271,
		"release_date": "2019-11-01",
		"promotional_set": False
	},
	{
		"series": "Sword & Shield Series",
		"name": "Sword & Shield",
		"cards": 216,
		"release_date": "2020-02-07",
		"promotional_set": False
	},
	{
		"series": "Sword & Shield Series",
		"name": "Rebel Clash",
		"cards": 209,
		"release_date": "2020-05-01",
		"promotional_set": False
	},
	{
		"series": "Sword & Shield Series",
		"name": "Darkness Ablaze",
		"cards": 201,
		"release_date": "2020-08-14",
		"promotional_set": False
	},
	{
		"series": "Sword & Shield Series",
		"name": "Vivid Voltage",
		"cards": 203,
		"release_date": "2020-11-13",
		"promotional_set": False
	},
	{
		"series": "Sword & Shield Series",
		"name": "Battle Styles",
		"cards": 183,
		"release_date": "2021-03-19",
		"promotional_set": False
	},
	{
		"series": "Sword & Shield Series",
		"name": "Chilling Reign",
		"cards": 233,
		"release_date": "2021-06-18",
		"promotional_set": False
	},
	{
		"series": "Sword & Shield Series",
		"name": "Evolving Skies",
		"cards": 237,
		"release_date": "2021-08-27",
		"promotional_set": False
	},
	{
		"series": "Sword & Shield Series",
		"name": "Fusion Strike",
		"cards": 284,
		"release_date": "2021-11-12",
		"promotional_set": False
	},
	{
		"series": "Sword & Shield Series",
		"name": "Brilliant Stars",
		"cards": 216,
		"release_date": "2022-02-25",
		"promotional_set": False
	},
	{
		"series": "Sword & Shield Series",
		"name": "Astral Radiance",
		"cards": 246,
		"release_date": "2022-05-27",
		"promotional_set": False
	},
	{
		"series": "Sword & Shield Series",
		"name": "Lost Origin",
		"cards": 247,
		"release_date": "2022-09-09",
		"promotional_set": False
	},
	{
		"series": "Sword & Shield Series",
		"name": "Silver Tempest",
		"cards": 245,
		"release_date": "2022-11-11",
		"promotional_set": False
	},
	{
		"series": "Scarlet & Violet Series",
		"name": "Scarlet & Violet",
		"cards": 198,
		"release_date": "2023-03-31",
		"promotional_set": False
	},
	{
		"series": "Special Expansions",
		"name": "Dragon Vault",
		"cards": 21,
		"release_date": "2012-10-05",
		"promotional_set": False
	},
	{
		"series": "Special Expansions",
		"name": "Double Crisis",
		"cards": 34,
		"release_date": "2015-03-25",
		"promotional_set": False
	},
	{
		"series": "Special Expansions",
		"name": "Generations",
		"cards": 115,
		"release_date": "2016-02-22",
		"promotional_set": False
	},
	{
		"series": "Special Expansions",
		"name": "Shining Legends",
		"cards": 78,
		"release_date": "2017-10-06",
		"promotional_set": False
	},
	{
		"series": "Special Expansions",
		"name": "Dragon Majesty",
		"cards": 78,
		"release_date": "2018-09-07",
		"promotional_set": False
	},
	{
		"series": "Special Expansions",
		"name": "Detective Pikachu",
		"cards": 18,
		"release_date": "2019-03-29",
		"promotional_set": False
	},
	{
		"series": "Special Expansions",
		"name": "Hidden Fates",
		"cards": 163,
		"release_date": "2019-08-23",
		"promotional_set": False
	},
	{
		"series": "Special Expansions",
		"name": "Champion's Path",
		"cards": 80,
		"release_date": "2020-09-25",
		"promotional_set": False
	},
	{
		"series": "Special Expansions",
		"name": "Shining Fates",
		"cards": 195,
		"release_date": "2021-02-19",
		"promotional_set": False
	},
	{
		"series": "Special Expansions",
		"name": "Celebrations",
		"cards": 50,
		"release_date": "2021-10-08",
		"promotional_set": False
	},
	{
		"series": "Special Expansions",
		"name": "Pok\u00e9mon GO",
		"cards": 88,
		"release_date": "2022-07-01",
		"promotional_set": False
	},
	{
		"series": "Special Expansions",
		"name": "Crown Zenith",
		"cards": 230,
		"release_date": "2023-01-20",
		"promotional_set": False
	},
	{
		"series": "Black Star Promos",
		"name": "Wizards Black Star Promos",
		"cards": 53,
		"release_date": "1999-07-01",
		"promotional_set": True
	},
	{
		"series": "Black Star Promos",
		"name": "Nintendo Series",
		"cards": 40,
		"release_date": "2003-10-01",
		"promotional_set": True
	},
	{
		"series": "Black Star Promos",
		"name": "Diamond and Pearl Series",
		"cards": 56,
		"release_date": "2007-05-01",
		"promotional_set": True
	},
	{
		"series": "Black Star Promos",
		"name": "HeartGold SoulSilver",
		"cards": 25,
		"release_date": "2010-02-01",
		"promotional_set": True
	},
	{
		"series": "Black Star Promos",
		"name": "Black and White Series",
		"cards": 101,
		"release_date": "2011-03-01",
		"promotional_set": True
	},
	{
		"series": "Black Star Promos",
		"name": "XY Black Star Promos",
		"cards": 211,
		"release_date": "2013-10-01",
		"promotional_set": True
	},
	{
		"series": "Black Star Promos",
		"name": "Sun and Moon Series",
		"cards": 248,
		"release_date": "2016-11-01",
		"promotional_set": True
	},
	{
		"series": "Black Star Promos",
		"name": "Sword and Shield Series",
		"cards": 305,
		"release_date": "2019-11-01",
		"promotional_set": True
	},
	{
		"series": "Black Star Promos",
		"name": "Scarlet & Violet Series",
		"cards": -1,
		"release_date": "2023-01-01",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "Southern Islands",
		"cards": 18,
		"release_date": "2001-07-31",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "Best of Game",
		"cards": 9,
		"release_date": "2002-12-01",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "Pok\u00e9 Card Creator Pack",
		"cards": 5,
		"release_date": "2004-07-01",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "POP Series 1",
		"cards": 17,
		"release_date": "2004-09-01",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "POP Series 2",
		"cards": 17,
		"release_date": "2005-08-01",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "POP Series 3",
		"cards": 17,
		"release_date": "2006-04-01",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "POP Series 4",
		"cards": 17,
		"release_date": "2006-08-01",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "POP Series 5",
		"cards": 17,
		"release_date": "2007-03-01",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "POP Series 6",
		"cards": 17,
		"release_date": "2007-09-01",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "POP Series 7",
		"cards": 17,
		"release_date": "2008-03-01",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "POP Series 8",
		"cards": 17,
		"release_date": "2008-09-01",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "POP Series 9",
		"cards": 17,
		"release_date": "2009-03-01",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "Pok\u00e9mon Rumble",
		"cards": 16,
		"release_date": "2009-12-02",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "McDonald's Collection",
		"cards": 12,
		"release_date": "2011-06-17",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "McDonald's Collection 2012",
		"cards": 12,
		"release_date": "2012-06-15",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "McDonald's Collection 2013",
		"cards": 12,
		"release_date": "2013-10-13",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "McDonald's Collection 2014",
		"cards": 12,
		"release_date": "2014-05-23",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "McDonald's Collection 2015",
		"cards": 12,
		"release_date": "2015-10-14",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "McDonald's Collection 2016",
		"cards": 12,
		"release_date": "2016-08-19",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "McDonald's Collection 2017",
		"cards": 12,
		"release_date": "2017-07-04",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "McDonald's Collection 2018 [French]",
		"cards": 40,
		"release_date": "2018-06-13",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "McDonald's Collection 2018 [English]",
		"cards": 12,
		"release_date": "2018-10-16",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "McDonald's Collection 2019 [English]",
		"cards": 12,
		"release_date": "2019-10-15",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "McDonald's Collection 2019 [French]",
		"cards": 40,
		"release_date": "2019-10-30",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "Pok\u00e9mon Futsal",
		"cards": 5,
		"release_date": "2020-09-11",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "McDonald's Collection 2021",
		"cards": 25,
		"release_date": "2021-02-09",
		"promotional_set": True
	},
	{
		"series": "Other Promotional Sets",
		"name": "McDonald's Collection 2022",
		"cards": 15,
		"release_date": "2022-08-03",
		"promotional_set": True
	}
]


def run():
	"""
	Populate expansion test data into the database
	"""
	try:
		for dictionary in expansion_data:
			Expansion.objects.create(**dictionary)
		print("Expansions populated successfully!")
	except IntegrityError:
		print("Some or all of the instances already exist in the database.")
