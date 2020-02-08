"""
us_tx_jails.py - Retrieve a list of TDCJ Jails in Texas.

These data were scraped from https://www.tdcj.texas.gov/unit_directory/
on Feb 7, 2020.

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from docassemble.base.util import Person, Address
from docassemble.base.logger import logmessage

JAILS = {
	"Allred": {
		"unit_name": "James V. Allred Unit",
		"telephone": "(940) 855-7477 (**069)",
		"address": "2101 FM 369 North",
		"city": " Iowa Park",
		"state": "TX",
		"zip": "76367",
	},
	"Bell": {
		"unit_name": "Oliver J. Bell Unit",
		"telephone": "(281) 592-9559",
		"address": "P.O. Box 1678",
		"city": " Cleveland",
		"state": "TX",
		"zip": "77328",
	},
	"Beto": {
		"unit_name": "George Beto Unit",
		"telephone": "(903) 928-2217 (**022)",
		"address": "1391 FM 3328",
		"city": " Tennessee Colony",
		"state": "TX",
		"zip": "75880",
	},
	"Boyd": {
		"unit_name": "William R. Boyd Unit",
		"telephone": "(254) 739-5555 (**051)",
		"address": "200 Spur 113",
		"city": " Teague",
		"state": "TX",
		"zip": "75860-20",
	},
	"Bradshaw": {
		"unit_name": "James Bradshaw State Jail",
		"telephone": "(903) 655-0880",
		"address": "P.O. Box 9000",
		"city": " Henderson",
		"state": "TX",
		"zip": "75653",
	},
	"Bridgeport": {
		"unit_name": "Bridgeport Correctional Center",
		"telephone": "(940) 683-3010 (**674)",
		"address": "4000 North Tenth Street",
		"city": " Bridgeport",
		"state": "TX",
		"zip": "76426",
	},
	"Briscoe": {
		"unit_name": "Dolph Briscoe Unit",
		"telephone": "(830) 965-4444 (**052)",
		"address": "1459 West Highway 85",
		"city": " Dilley",
		"state": "TX",
		"zip": "78017",
	},
	"Byrd": {
		"unit_name": 'James "Jay H. Byrd Unit',
		"telephone": "(936) 295-5768 (**008)",
		"address": "21 FM 247",
		"city": " Huntsville",
		"state": "TX",
		"zip": "77320",
	},
	"Clemens": {
		"unit_name": "Clemens Unit",
		"telephone": "(979) 798-2188 (**005)",
		"address": "11034 Hwy 36",
		"city": " Brazoria",
		"state": "TX",
		"zip": "77422",
	},
	"Clements": {
		"unit_name": "William P. Clements Unit",
		"telephone": "(806) 381-7080 (**037)",
		"address": "9601 Spur 591",
		"city": " Amarillo",
		"state": "TX",
		"zip": "79107-96",
	},
	"Coffield": {
		"unit_name": "H. H. Coffield Unit",
		"telephone": "(903) 928-2211 (**006)",
		"address": "2661 FM 2054",
		"city": " Tennessee Colony",
		"state": "TX",
		"zip": "75884",
	},
	"Cole": {
		"unit_name": "Buster Cole State Jail",
		"telephone": "(903) 583-1100 (**102)",
		"address": "3801 Silo Road",
		"city": " Bonham",
		"state": "TX",
		"zip": "75418",
	},
	"Connally": {
		"unit_name": "John B. Connally Unit",
		"telephone": "(830) 583-4003 (**068)",
		"address": "899 FM 632",
		"city": " Kenedy",
		"state": "TX",
		"zip": "78119",
	},
	"Cotulla": {
		"unit_name": "Cotulla Transfer Facility",
		"telephone": "(830) 879-3077 (**061)",
		"address": "610 FM 624",
		"city": " Cotulla",
		"state": "TX",
		"zip": "78014",
	},
	"Crain": {
		"unit_name": "Christina Melton Crain Unit",
		"telephone": "(254) 865-8431 (**024)",
		"address": "1401 State School Road",
		"city": " Gatesville",
		"state": "TX",
		"zip": "76599-29",
	},
	"Dalhart": {
		"unit_name": "Dalhart Unit",
		"telephone": "(806) 249-8655 (**072)",
		"address": "11950 FM 998",
		"city": " Dalhart",
		"state": "TX",
		"zip": "79022",
	},
	"Daniel": {
		"unit_name": "Price Daniel Unit",
		"telephone": "(325) 573-1114 (**038)",
		"address": "938 South FM 1673",
		"city": " Snyder",
		"state": "TX",
		"zip": "79549",
	},
	"Darrington": {
		"unit_name": "Darrington Unit",
		"telephone": "(281) 595-3465 (**007)",
		"address": "59 Darrington Road",
		"city": " Rosharon",
		"state": "TX",
		"zip": "77583",
	},
	"Diboll": {
		"unit_name": "Diboll Correctional Center",
		"telephone": "(936) 829-2295",
		"address": "1604 South First Street",
		"city": " Diboll",
		"state": "TX",
		"zip": "75941",
	},
	"Dominguez": {
		"unit_name": "Fabian Dale Dominguez State Jail",
		"telephone": "(210) 675-6620 (**098)",
		"address": "6535 Cagnon Road",
		"city": " San Antonio",
		"state": "TX",
		"zip": "78252-22",
	},
	"Duncan": {
		"unit_name": "Rufus H. Duncan Geriatric Facility",
		"telephone": "(936) 829-2616 (**063)",
		"address": "1502 South First Street",
		"city": " Diboll",
		"state": "TX",
		"zip": "75941",
	},
	"East Texas": {
		"unit_name": "East Texas Multi-Use Facility",
		"telephone": "(903) 655-3300",
		"address": "900 Industrial Drive",
		"city": " Henderson",
		"state": "TX",
		"zip": "75652",
	},
	"Eastham": {
		"unit_name": "Eastham Unit",
		"telephone": "(936) 636-7321 (**009)",
		"address": "2665 Prison Road #1",
		"city": " Lovelady",
		"state": "TX",
		"zip": "75851",
	},
	"Ellis": {
		"unit_name": "O.B. Ellis Unit",
		"telephone": "(936) 295-5756 (**010)",
		"address": "1697 FM 980",
		"city": " Huntsville",
		"state": "TX",
		"zip": "77343",
	},
	"Estelle": {
		"unit_name": 'W. J. "Jim" Estelle Unit',
		"telephone": "(936) 291-4200 (**032)",
		"address": "264 FM 3478",
		"city": " Huntsville",
		"state": "TX",
		"zip": "77320-33",
	},
	"Estes": {
		"unit_name": 'Sanders "Sandy" Estes Unit"',
		"telephone": "(972) 366-3334 (**670)",
		"address": "1100 Hwy 1807",
		"city": " Venus",
		"state": "TX",
		"zip": "76084",
	},
	"Ferguson": {
		"unit_name": "Jim Ferguson Unit",
		"telephone": "(936) 348-3751 (**011)",
		"address": "12120 Savage Drive",
		"city": " Midway",
		"state": "TX",
		"zip": "75852",
	},
	"Formby": {
		"unit_name": "Formby State Jail",
		"telephone": "(806) 296-2448 (**106)",
		"address": "998 County Road AA",
		"city": " Plainview",
		"state": "TX",
		"zip": "79072",
	},
	"Fort Stockton": {
		"unit_name": "Fort Stockton Transfer Facility",
		"telephone": "(432) 336-7676 (**062)",
		"address": "1536 IH-10 East",
		"city": " Fort Stockton",
		"state": "TX",
		"zip": "79735",
	},
	"Garza East": {
		"unit_name": "Garza East Transfer Facility",
		"telephone": "(361) 358-9880 (**096)",
		"address": "4304 Highway 202",
		"city": " Beeville",
		"state": "TX",
		"zip": "78102",
	},
	"Garza West": {
		"unit_name": "Garza West Transfer Facility",
		"telephone": "(361) 358-9890 (**095)",
		"address": "4250 Highway 202",
		"city": " Beeville",
		"state": "TX",
		"zip": "78102",
	},
	"Gist": {
		"unit_name": "Larry Gist State Jail",
		"telephone": "(409) 727-8400 (**097)",
		"address": "3295 FM 3514",
		"city": " Beaumont",
		"state": "TX",
		"zip": "77705",
	},
	"Glossbrenner": {
		"unit_name": "Ernestine Glossbrenner Unit",
		"telephone": "(361) 279-2705 (**088)",
		"address": "5100 South FM 1329",
		"city": " San Diego",
		"state": "TX",
		"zip": "78384",
	},
	"Goodman": {
		"unit_name": "Glen Ray Goodman Transfer Facility",
		"telephone": "(409) 383-0012 (**086)",
		"address": "349 Private Road 8430",
		"city": "  Jasper",
		"state": "TX",
		"zip": "75951",
	},
	"Goree": {
		"unit_name": "Thomas Goree Unit",
		"telephone": "(936) 295-6331 (**012)",
		"address": "7405 Hwy 75 South",
		"city": " Huntsville",
		"state": "TX",
		"zip": "77344",
	},
	"Gurney": {
		"unit_name": "Joe F. Gurney Transfer Facility",
		"telephone": "(903) 928-3118 (**094)",
		"address": "1385 FM 3328",
		"city": " Palestine",
		"state": "TX",
		"zip": "75803",
	},
	"Halbert": {
		"unit_name": "Ellen Halbert Unit",
		"telephone": "(512) 756-6171 (**084)",
		"address": "800 Ellen Halbert Drive",
		"city": " Burnet",
		"state": "TX",
		"zip": "78611",
	},
	"Hamilton": {
		"unit_name": "J. W. Hamilton Unit",
		"telephone": "(979) 779-1633 (**077)",
		"address": "200 Lee Morrison Lane",
		"city": " Bryan",
		"state": "TX",
		"zip": "77807",
	},
	"Havins": {
		"unit_name": "Thomas R. Havins Unit",
		"telephone": "(325) 643-5575 (**082)",
		"address": "500 FM 45 East",
		"city": " Brownwood",
		"state": "TX",
		"zip": "76801",
	},
	"Henley": {
		"unit_name": "Dempsie Henley State Jail",
		"telephone": "(936) 258-2476 (**083)",
		"address": "7581 Hwy 321",
		"city": " Dayton",
		"state": "TX",
		"zip": "77535",
	},
	"Hightower": {
		"unit_name": "L.V. Hightower Unit",
		"telephone": "(936) 258-8013 (**041)",
		"address": "902 FM 686",
		"city": " Dayton",
		"state": "TX",
		"zip": "77535",
	},
	"Hilltop": {
		"unit_name": "Hilltop Unit",
		"telephone": "(254) 865-8901 (**031)",
		"address": "1500 State School Road",
		"city": " Gatesville",
		"state": "TX",
		"zip": "76598-2",
	},
	"Hobby": {
		"unit_name": "William P. Hobby Unit",
		"telephone": "(254) 883-5561 (**039)",
		"address": "742 FM 712",
		"city": " Marlin",
		"state": "TX",
		"zip": "76661",
	},
	"Hodge": {
		"unit_name": "Jerry H. Hodge Unit",
		"telephone": "(903) 683-5781 (**075)",
		"address": "379 FM 2972 West",
		"city": " Rusk",
		"state": "TX",
		"zip": "75785-36",
	},
	"Holliday": {
		"unit_name": "Reverend C.A. Holliday Transfer Facility",
		"telephone": "(936) 295-8200 (**092)",
		"address": "295 IH-45 North",
		"city": " Huntsville",
		"state": "TX",
		"zip": "77320-84",
	},
	"Hospital Galveston": {
		"unit_name": "Hospital Galveston",
		"telephone": "(409) 772-2875 (**023)",
		"address": "P.O. Box 48 Substation #1",
		"city": "Galveston",
		"state": "TX",
		"zip": "77555",
	},
	"Hughes": {
		"unit_name": "Alfred D. Hughes Unit",
		"telephone": "(254) 865-6663 (**042)",
		"address": "Route 2 Box 4400",
		"city": " Gatesville",
		"state": "TX",
		"zip": "76597",
	},
	"Huntsville": {
		"unit_name": "Huntsville Unit",
		"telephone": "(936) 437-1555 (**013)",
		"address": "815 12th Street",
		"city": " Huntsville",
		"state": "TX",
		"zip": "77348",
	},
	"Hutchins": {
		"unit_name": "Hutchins State Jail",
		"telephone": "(972) 225-1304 (**099)",
		"address": "1500 East Langdon Road",
		"city": " Dallas",
		"state": "TX",
		"zip": "75241",
	},
	"Jester I": {
		"unit_name": "Beauford H. Jester I Unit",
		"telephone": "(281) 277-3030 (**014)",
		"address": "1 Jester Road",
		"city": " Richmond",
		"state": "TX",
		"zip": "77406",
	},
	"Jester III": {
		"unit_name": "Beauford H. Jester III Unit",
		"telephone": "(281) 277-7000 (**030)",
		"address": "3 Jester Road",
		"city": " Richmond",
		"state": "TX",
		"zip": "77406",
	},
	"Jester IV": {
		"unit_name": "Beauford H. Jester IV Unit",
		"telephone": "(281) 277-3700 (**033)",
		"address": "4 Jester Road",
		"city": " Richmond",
		"state": "TX",
		"zip": "77406",
	},
	"Johnston": {
		"unit_name": "Clyde M. Johnston Unit",
		"telephone": "(903) 342-6166 (**089)",
		"address": "703 Airport Road",
		"city": " Winnsboro",
		"state": "TX",
		"zip": "75494",
	},
	"Jordan": {
		"unit_name": "Rufe Jordan Unit / Baten Intermediate Sanction Facility",
		"telephone": "(806) 665-7070 (**056)",
		"address": "1992 Helton Road",
		"city": " Pampa",
		"state": "TX",
		"zip": "79065",
	},
	"Kyle": {
		"unit_name": "Kyle Correctional Center",
		"telephone": "(512) 268-0079 (**633)",
		"address": "23001 IH-35",
		"city": " Kyle",
		"state": "TX",
		"zip": "78640",
	},
	"LeBlanc": {
		"unit_name": "Richard P. LeBlanc Unit",
		"telephone": "(409) 724-1515 (**076)",
		"address": "3695 FM 3514",
		"city": " Beaumont",
		"state": "TX",
		"zip": "77705",
	},
	"Lewis": {
		"unit_name": "Gib Lewis Unit",
		"telephone": "(409) 283-8181 (**040)",
		"address": "777 FM 3497",
		"city": " Woodville",
		"state": "TX",
		"zip": "75990",
	},
	"Lindsey": {
		"unit_name": "John R. Lindsey State Jail",
		"telephone": "(940) 567-2272",
		"address": "1620 FM 3344",
		"city": " Jacksboro",
		"state": "TX",
		"zip": "76458",
	},
	"Lockhart": {
		"unit_name": "Lockhart Correctional Facility",
		"telephone": "(512) 398-3480 (**109)",
		"address": "1400 Industrial Blvd",
		"city": " Lockhart",
		"state": "TX",
		"zip": "78644",
	},
	"Lopez": {
		"unit_name": "Reynoldo V. Lopez State Jail",
		"telephone": "(956) 316-3810 (**103)",
		"address": "1203 El Cibolo Road",
		"city": " Edinburg",
		"state": "TX",
		"zip": "78542",
	},
	"Luther": {
		"unit_name": "O.L. Luther Unit",
		"telephone": "(936) 825-7547 (**029)",
		"address": "1800 Luther Drive",
		"city": " Navasota",
		"state": "TX",
		"zip": "77868",
	},
	"Lychner": {
		"unit_name": "Pam Lychner State Jail",
		"telephone": "(281) 454-5036 (**100)",
		"address": "2350 Atascocita Road",
		"city": " Humble",
		"state": "TX",
		"zip": "77396",
	},
	"Lynaugh": {
		"unit_name": "James Lynaugh Unit",
		"telephone": "(432) 395-2938 (**073)",
		"address": "1098 South Highway 2037",
		"city": " Fort Stockton",
		"state": "TX",
		"zip": "79735",
	},
	"Marlin": {
		"unit_name": "Marlin Transfer Facility",
		"telephone": "(254) 883-3858 (**064)",
		"address": "2893 State Hwy 6",
		"city": " Marlin",
		"state": "TX",
		"zip": "76661-65",
	},
	"McConnell": {
		"unit_name": "William G. McConnell Unit",
		"telephone": "(361) 362-2300 (**048)",
		"address": "3001 South Emily Drive",
		"city": " Beeville",
		"state": "TX",
		"zip": "78102",
	},
	"Michael": {
		"unit_name": "Mark W. Michael Unit",
		"telephone": "(903) 928-2311 (**036)",
		"address": "2664 FM 2054",
		"city": " Tennessee Colony",
		"state": "TX",
		"zip": "75886",
	},
	"Middleton": {
		"unit_name": "John Middleton Transfer Facility",
		"telephone": "(325) 548-9075 (**093)",
		"address": "13055 FM 3522",
		"city": " Abilene",
		"state": "TX",
		"zip": "79601",
	},
	"Montford/West Texas Hospital": {
		"unit_name": "John Montford  Unit",
		"telephone": "(806) 745-1021 (**090)",
		"address": "8602 Peach Street",
		"city": " Lubbock",
		"state": "TX",
		"zip": "79404",
	},
	"Moore, B.": {
		"unit_name": "Billy Moore Correctional Center",
		"telephone": "(903) 834-6186",
		"address": "8500 North FM 3053",
		"city": " Overton",
		"state": "TX",
		"zip": "75684",
	},
	"Moore, C.": {
		"unit_name": "Choice Moore Transfer Facility",
		"telephone": "(903) 583-4464 (**079)",
		"address": "1700 North FM 87",
		"city": " Bonham",
		"state": "TX",
		"zip": "75418",
	},
	"Mountain View": {
		"unit_name": "Mountain View Unit",
		"telephone": "(254) 865-7226 (**016)",
		"address": "2305 Ransom Road",
		"city": " Gatesville",
		"state": "TX",
		"zip": "76528",
	},
	"Murray": {
		"unit_name": "Dr. Lane Murray Unit",
		"telephone": "(254) 865-2000 (**105)",
		"address": "1916 North Hwy 36 Bypass",
		"city": " Gatesville",
		"state": "TX",
		"zip": "76596",
	},
	"Neal": {
		"unit_name": "Nathaniel J. Neal Unit",
		"telephone": "(806) 383-1175 (**070)",
		"address": "9055 Spur 591",
		"city": " Amarillo",
		"state": "TX",
		"zip": "79107-96",
	},
	"Ney": {
		"unit_name": "Joe Ney State Jail",
		"telephone": "(830) 426-8030 (**085)",
		"address": "114 Private Road 4303",
		"city": " Hondo",
		"state": "TX",
		"zip": "78861-3",
	},
	"Pack": {
		"unit_name": "Wallace Pack Unit",
		"telephone": "(936) 825-3728 (**026)",
		"address": "2400 Wallace Pack Road",
		"city": " Navasota",
		"state": "TX",
		"zip": "77868",
	},
	"Plane/Santa Maria Baby Bonding": {
		"unit_name": "Lucile Plane State Jail",
		"telephone": "(936) 258-2476 (**101)",
		"address": "904 FM 686",
		"city": " Dayton",
		"state": "TX",
		"zip": "77535",
	},
	"Polunsky": {
		"unit_name": "Allan B. Polunsky Unit",
		"telephone": "(936) 967-8082 (**054)",
		"address": "3872 FM 350 South",
		"city": " Livingston",
		"state": "TX",
		"zip": "77351",
	},
	"Powledge": {
		"unit_name": "Louis C. Powledge Unit",
		"telephone": "(903) 723-5074 (**028)",
		"address": "1400 FM 3452",
		"city": " Palestine",
		"state": "TX",
		"zip": "75803",
	},
	"Ramsey": {
		"unit_name": "W. F. Ramsey Unit",
		"telephone": "(281) 595-3491 (**017)",
		"address": "1100 FM 655",
		"city": " Rosharon",
		"state": "TX",
		"zip": "77583",
	},
	"Roach": {
		"unit_name": "T.L. Roach Unit",
		"telephone": "(940) 937-6364 (**050)",
		"address": "15845 FM 164",
		"city": " Childress",
		"state": "TX",
		"zip": "79201",
	},
	"Robertson": {
		"unit_name": "French Robertson Unit",
		"telephone": "(325) 548-9035 (**047)",
		"address": "12071 FM 3522",
		"city": " Abilene",
		"state": "TX",
		"zip": "79601",
	},
	"San Saba": {
		"unit_name": "San Saba Transfer Facility",
		"telephone": "(325) 372-4255 (**65)",
		"address": "206 South Wallace Creek Road",
		"city": " San Saba",
		"state": "TX",
		"zip": "76877",
	},
	"Sanchez": {
		"unit_name": "Rogelio Sanchez State Jail",
		"telephone": "(915) 856-0046 (**108)",
		"address": "3901 State Jail Road",
		"city": " El Paso",
		"state": "TX",
		"zip": "79938-84",
	},
	"Sayle": {
		"unit_name": "Walker Sayle Unit",
		"telephone": "(254) 559-1581 (**080)",
		"address": "4176 FM 1800",
		"city": " Breckenridge",
		"state": "TX",
		"zip": "76424-73",
	},
	"Scott": {
		"unit_name": "Wayne Scott Unit",
		"telephone": "(979) 849-9306 (**019)",
		"address": "6999 Retrieve",
		"city": " Angleton",
		"state": "TX",
		"zip": "77515",
	},
	"Segovia": {
		"unit_name": "Manuel A. Segovia Unit",
		"telephone": "(956) 316-2400 (**078)",
		"address": "1201 E. El Cibolo Road",
		"city": " Edinburg",
		"state": "TX",
		"zip": "78542",
	},
	"Skyview": {
		"unit_name": "Skyview Unit",
		"telephone": "(903) 683-5781 (**034)",
		"address": "379 FM 2972 West",
		"city": " Rusk",
		"state": "TX",
		"zip": "75785-36",
	},
	"Smith": {
		"unit_name": "Preston E. Smith Unit",
		"telephone": "(806) 872-6741 (**053)",
		"address": "1313 CR 19",
		"city": " Lamesa",
		"state": "TX",
		"zip": "79331-18",
	},
	"Stevenson": {
		"unit_name": "Clarence N. Stevenson Unit",
		"telephone": "(361) 275-2075 (**071)",
		"address": "1525 FM 766",
		"city": " Cuero",
		"state": "TX",
		"zip": "77954",
	},
	"Stiles": {
		"unit_name": "Mark W. Stiles Unit",
		"telephone": "(409) 722-5255 (**049)",
		"address": "3060 FM 3514",
		"city": " Beaumont",
		"state": "TX",
		"zip": "77705",
	},
	"Stringfellow": {
		"unit_name": 'A.M. "Mac" Stringfellow Unit',
		"telephone": "(281) 595-3413 (**018)",
		"address": "1200 FM 655",
		"city": " Rosharon",
		"state": "TX",
		"zip": "77583",
	},
	"Telford": {
		"unit_name": "Barry B. Telford Unit",
		"telephone": "(903) 628-3171 (**067)",
		"address": "3899  Hwy 98",
		"city": " New Boston",
		"state": "TX",
		"zip": "75570",
	},
	"Terrell": {
		"unit_name": "C.T. Terrell Unit",
		"telephone": "(281) 595-3481 (**027)",
		"address": "1300 FM 655",
		"city": " Rosharon",
		"state": "TX",
		"zip": "77583",
	},
	"Torres": {
		"unit_name": "Ruben M. Torres Unit",
		"telephone": "(830) 426-5325 (**055)",
		"address": "125 Private Road 4303",
		"city": " Hondo",
		"state": "TX",
		"zip": "78861",
	},
	"Travis County": {
		"unit_name": "Travis County State Jail",
		"telephone": "(512) 926-4482 (**118)",
		"address": "8101 FM 969",
		"city": " Austin",
		"state": "TX",
		"zip": "78724",
	},
	"Tulia": {
		"unit_name": "Tulia Transfer Facility",
		"telephone": "(806) 995-4109 (**066)",
		"address": "4000 Highway 86 West",
		"city": " Tulia",
		"state": "TX",
		"zip": "79088",
	},
	"Vance": {
		"unit_name": "Carol S. Vance Unit",
		"telephone": "(281) 277-3030 (**015)",
		"address": "2 Jester Road",
		"city": " Richmond",
		"state": "TX",
		"zip": "77406",
	},
	"Wallace/San Angelo Work Camp": {
		"unit_name": "Daniel Webster Wallace Unit",
		"telephone": "(325) 728-2162 (**074)",
		"address": "1675 South FM 3525",
		"city": " Colorado City",
		"state": "TX",
		"zip": "79512",
	},
	"Wheeler": {
		"unit_name": "J.B. Wheeler State Jail",
		"telephone": "(806) 293-1081 (**087)",
		"address": "986 County Road AA",
		"city": " Plainview",
		"state": "TX",
		"zip": "79072",
	},
	"Willacy County": {
		"unit_name": "Willacy County State Jail",
		"telephone": "(956) 689-4900",
		"address": "1695 South Buffalo Drive",
		"city": " Raymondville",
		"state": "TX",
		"zip": "78580",
	},
	"Woodman": {
		"unit_name": "Linda Woodman State Jail",
		"telephone": "(254) 865-9398 (**107)",
		"address": "1210 Coryell City Road",
		"city": " Gatesville",
		"state": "TX",
		"zip": "76528",
	},
	"Wynne": {
		"unit_name": "John M. Wynne Unit",
		"telephone": "(936) 295-9126 (**020)",
		"address": "810 FM 2821",
		"city": " Huntsville",
		"state": "TX",
		"zip": "77349",
	},
	"Young": {
		"unit_name": "Carole S. Young Medical Facility",
		"telephone": "(409) 948-0001 (**129)",
		"address": "5509 Attwater Ave.",
		"city": " Dickinson",
		"state": "TX",
		"zip": "77539",
	},
}


class UsTxJails(object):
	"""
	A database of Texas Department of Corrections Facilities.
	"""
	def get_jails(self) -> list:
		"""
		Returns:
			(list): A list of jails operated by the state
		"""
		the_list = [{short_name: self.make_jail(jail)} for short_name, jail in JAILS.items()]
		return the_list

	def get_jail(self, short_name: str) -> Person:
		"""
		Return a given jail.

		Args:
			short_name (str): Key into the JAILS dict
		Returns:
			(Person): Name and address of the requested jail facility
		"""
		jail = JAILS.get(short_name, None)
		if not jail:
			return None

		return self.make_jail(jail)

	def make_jail(self, jail: dict) -> Person:
		"""
		Make a jail from a dict.
		"""
		address = Address(
			address = jail['address'],
			city = jail['city'],
			state = jail['state'],
			zip = jail['zip']
		)

		result = Person(address=address, name=str(jail['unit_name']))

		return result
