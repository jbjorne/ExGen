# Harjoitus: Roskapostisuodatin

Rakennetaan roskapostisuodatin, joka suodattaa viestit otsikon perusteella, käyttäen lähimmän naapurin menetelmää. Käytössä on seuraava aineisto, jolle on määritelty roskapostiluokka (kyllä tai ei):

* [email1]()
* [email2]()
* [email3]()
* [email4]()
* [email5]()
* [email6]()
* [email7]()

Aineiston viestit 1-5 muodostavat koulutusaineiston ja 6-7 testiaineiston. Jotta lähimmän naapurin menetelmä voisi käsitellä aineistoa, esimerkit pitää muuntaa piirrevektoreiksi.Roskapostisuodattimelle on tähän tarkoitukseen laadittu avainsanakartta:

** [key1](), [key2](), [key3](), [key4](), [key5]() **

Avainsanakartan jokainen sana vastaa piirrevektorin yhtä ulottuvuutta (vasemmalta oikealle). Piirrevektori esitetään muodossa xxxxx jossa jokainen ulottuvuus voi olla olemassa (1) tai ei (0). Sähköpostiviestin piirrevektori voi siis olla esimerkiksi [00101](example).

## Tehtävä 

Määritä annetuille sähköposteille piirrevektorit käyttämällä avainsanakarttaa (isoilla ja pienillä kirjaimilla tai välimerkeillä ei ole merkitystä, mutta muuten sanan täytyy vastata täsmälleen aineiston sanaa).

* [vector1](answer)
* [vector2](answer)
* [vector3](answer)
* [vector4](answer)
* [vector5](answer)
* [vector6](answer)
* [vector7](answer)

## Tehtävä

Määritä testiaineiston vektoreiden (6 ja 7) etäisyys (esimerkiksi [2](example)) jokaiseen koulutusaineiston vektoriin käyttäen Manhattan-etäisyyttä.

* d(1,6)=[d16](answer) d(1,7)=[d17](answer)
* d(2,6)=[d26](answer) d(2,7)=[d27](answer)
* d(3,6)=[d36](answer) d(3,7)=[d37](answer)
* d(4,6)=[d46](answer) d(4,7)=[d47](answer)
* d(5,6)=[d56](answer) d(5,7)=[d57](answer)

Kun etäisyyksiä käytetään lähimmän naapurin menetelmässä, tarkastellaan aineistoa esimerkkien numerojärjestyksessä. Jos on useita lähimpiä naapureita, otetaan niistä ensimmäinen (tai ensimmäiset) numerojärjestyksessä.

## Tehtävä

Mitkä luokat lähimmän naapurin menetelmä ennustaisi testiesimerkeille?

* Ennuste esimerkille 6: [nn6](answer)
* Ennuste esimerkille 7: [nn7](answer)

## Tehtävä

Mitkä luokat kolmen lähimmän naapurin menetelmä (KNN, k=3) ennustaisi testiesimerkeille?

* Ennuste esimerkille 6: [knn6](answer)
* Ennuste esimerkille 7: [knn7](answer)

[](solution:begin)

Tehtävässä nähdään, miten piirteiden suunnittelu (feature engineering) toimii. Piirrevektoreiden rakentamisessa on hyvä huomata, miten sopimuksenvaraista esimerkiksi luonnollisen kielen muuttaminen koneen ymmärtämään muotoon on. Avainsanakartta on todennäköisesti laadittu katselemalla aineistoa ja päättelemällä, mitkä olisivat toimivia avainsanoja. Oikeassa tekstinlouhintajärjestelmässä piirteitä olisi huomattavasti enemmän, jopa tuhansia, ja niitä tuotettaisiin erilaisilla säännöillä, esim. roskapostisuodattimen yksittäinen piirre voisi merkitä sitä, että tekstissä on sana, jossa on numeroita kirjainten keskellä, koska roskapostittajat pyrkivät kiertämään avainsanojen tunnistusta tyyliin 'v1agra'. Tällaisia piirteitä, jotka joko löytyvät tai eivät löydy esimerkistä (eli ovat 1 tai 0) kutsutaan kategorisiksi piirteiksi.

Piirrevektorin toiminnassa oleellista on, että tietokoneen havaitsema samankaltaisuus perustuu samojen ulottuvuuksien "päällekkäisyyteen". Laadittaessa piirrevektoreita otsikoille, onkin tärkeää tarkastaa jokainen avainsana oikeassa järjestyksessä, ja huolellisesti merkitä 1 tai 0 oikean ulottuvuuden kohdalle, niin että lopullisessa vektorissa on aina viisi numeroa.

Esimerkkien etäisyys lasketaan Manhattan-etäisyytenä (se voisi yhtä hyvin olla esim. euklidinen tai kosinietäisyys). Koska vektoreiden arvot ovat joko nollia tai ykkösiä, Manhattan-etäisyyden laskeminen pelkistyy siihen, että lasketaan kuinka monta sellaista ulottuvuutta on, joissa vektoreilla on eri arvo.

Lähimmän naapurin löytäminen onnistuukin tämän jälkeen vain käymällä läpi etäisyyslistaa. Jos lähimpiä naapureita on useampi, ei ole mitään varsinaista sääntöä, miten luokka pitäisi valita, joten tällöin voidaan ottaa vaikka satunnainen lähin esimerkki. KNN menetelmässä useampi lähin naapuri menee luonnollisesti lähimpien naapureiden joukkoon, ja kun `k = 3` niin lähimpien naapureiden joukossa on aina yksiselitteisesti yleisin luokka (kun luokkia on kaksi).

[](solution:end)