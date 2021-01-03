Hilavitkutin Oy markkinoi uutta tuotettaan puhelinmyynnillä. Myyntityön nopeuttamiseksi puheluja soitetaan uusille asiakkaille, jotka muistuttavat aikaisemmin tuotteita ostaneita henkilöitä. Tällaiset henkilöt löydetään henkilötietokannasta lähimmän naapurin menetelmällä.

Piirrevektori koostetaan järjestyksessä seuraavista kategorisista muuttujista:

* sukupuoli (0=mies, 1=nainen)
* ikäryhmä (0 jos ikä on alle 30, muuten 1)
* asuinpaikka (0=muu maa, 1=Helsinki)
* lapsia (0=ei, 1=kyllä)
* siviilisääty (0=naimaton, 1=naimisissa)

Esimerkin luokka (0, 1 tai 2) määritellään siten, että luokka on 0, jos ostotapahtumia on korkeintaan 5, luokka on 1, jos ostotapahtumia on korkeintaan 10, ja muuten luokka on 2.

[](asiakkaat)

Muodosta piirrevektorit asiakasaineistolle. Piirrevektori esitetään muodossa xxxxx, joten piirrevektori voisi siis olla esimerkiksi [00101](example).

* Piirrevektori 1: [vec1](answer)
* Piirrevektori 2: [vec2](answer)
* Piirrevektori 3: [vec3](answer)
* Piirrevektori 4: [vec4](answer)
* Piirrevektori 5: [vec5](answer)
* Piirrevektori 6: [vec6](answer)

Laske testiaineiston esimerkkien (henkilöt 5 ja 6) Manhattan-etäisyydet koulutusaineiston esimerkkeihin (henkilöt 1-4):

* Etäisyys 1-5: [dist5-1](answer)
* Etäisyys 2-5: [dist5-2](answer)
* Etäisyys 3-5: [dist5-3](answer)
* Etäisyys 4-5: [dist5-4](answer)

* Etäisyys 1-6: [dist6-1](answer)
* Etäisyys 2-6: [dist6-2](answer)
* Etäisyys 3-6: [dist6-3](answer)
* Etäisyys 4-6: [dist6-4](answer)

Käyttäen lähimmän naapurin menetelmää, ennusta testiaineiston esimerkkien luokka:

* Esimerkin 5 ennustettu luokka: [class5](answer)
* Esimerkin 6 ennustettu luokka: [class6](answer)

