# Rajapinnat

## Uuden tapahtuman tallennus

* Toteutuksen prioriteetti: 1
* Toteutuksen tila: toteutettu :white_check_mark:
* HTTP Method: `POST`
* URL: `/v1/event`
* Onnistuneen kutsun statuskoodi: `HTTP 201`
* Onnistuneen kutsun paluuarvo: luodun tapahtuman yksilöllinen id

Esimerkki lähetettävästä datasta:
```JSON
{
 "device_id": 10123,
 "place_id": 945,
 "time": "2016-04-10T12:49:12+22:45",
 "type": "obscured",
 "value": 1.0
}
```

* `timestamp`-kenttä on valinnainen.  Oletusarvo vastaanottohetki.
* `place_id`-kenttä on valinnainen.  Oletuksena palvelu liittää samaan
  paikkaan, kuin aiempi data samasta anturista. Palauttaa `HTTP 409`
  viestillä `No previous event for device 10123` jos samalle anturille
  ei ole vielä yhtään tapahtumaa.
* `type`-kentän arvoja ovat ainakin: "occupied", "ambient_light",
  "movement", "obscured"
  * "occupied" on tarkoitettu antureille, jotka haluavat itse päätellä,
    onko paikassa joku.  Muut parametrit ovat antureiden raakadataa.
  * "ambient_light" tarkoittaa, kuinka kirkasta ympärillä oleva valo on.
  * "movement" tarkoittaa, kuinka paljon tilassa on havaittu liikettä.
  * "obscured" tarkoittaa, onko sähkösilmän edessä tyhjää vai este.
  * "closed" tarkoittaa, onko anturin seuraama ovi (tai ikkuna) kiinni
    vai auki.

## Tapahtumien raakadatan haku

* Toteutuksen prioriteetti: 1
* Toteutuksen tila: toteutettu kaikki prioriteetit :white_check_mark:
* HTTP Method: `GET`
* URL: `/v1/event/`
* Query-parametrit:
  * `starting` (prioriteetti 2): jättää pois tätä aiemmat tapahtumat,
    oletusarvo äärettömän kaukana menneisyydessä.
  * `ending` (prioriteetti 2): jättää pois tätä myöhemmät tapahtumat,
    oletusarvo äärettömän kaukana tulevaisuudessa
    * `starting` ja `ending` pitää olla ISO DateTime formaatissa `yyyy-MM-dd'T'HH:mm:ss.SSSZ` mutta kellonajan voi antaa epätarkempanakin, kuten esim. `2016-05-24T20:40`. Aikavyöhyke tosin katsotaan Herokun JVM-ajoympäristön asetuksista joten se voi olla mikä vaan. 
  * `device_id` (prioriteetti 3): haluttu anturi, toistettavissa
  * `place_id` (prioriteetti 3): haluttu paikka, toistettavissa
    * jos `device_id` tai `place_id` annetaan useamman kerran, kaikki
      luetellut paikat ja anturit haetaan.  Jos kumpaakaan ei anneta,
      haetaan kaikki paikat ja anturit.
    * useamman arvon syöttö tapahtuu monistamalla saman nimistä parametria, esim. `/v1/event?device_id=100&device_id=200`
  * `type` (prioriteetti 2): haluttu mittaustyyppi, oletuksena kaikki,
    toistettavissa
* Onnistuneen kutsun vastaus: `HTTP 200`

Esimerkki palautettavasta datasta:
```JSON
[{
 "id": 3579,
 "device_id": 10123,
 "place_id": 945,
 "timestamp": "2016-04-10T12:49:12+22:45",
 "type": "occupied",
 "value": 1.0
}, {
 "id": 7633,
 "device_id": 10456,
 "place_id": 945,
 "timestamp": "2016-03-10T12:49:12+22:45",
 "type": "ambient light",
 "value": 1030.07
}]
```

## Kaikkien paikkojen tämän hetken tilanteen selvitys

* Toteutuksen prioriteetti: 1
* Toteutuksen tila: toteutettu (tukee vain `occupied` tapahtumatyyppiä) :white_check_mark:
* HTTP Method: `GET`
* URL: `/v1/status/current`
* Query-parametrit:
  * `type` (prioriteetti 4): minkätyyppistä mittausdataa haetaan,
    oletuksena "occupied"
* Onnistuneen kutsun vastaus: `HTTP 200`

Esimerkkidata:
```JSON
[{
 "place_id": 945,
 "latitude": 24.93876,
 "longitude": 60.17664,
 "occupied": true
}, {
 "place_id": 946,
 "latitude": 24.93866,
 "longitude": 60.17664,
 "occupied": false
}]
```

## Paikan lisäys

* Toteutuksen prioriteetti: 1
* Toteutuksen tila: toteutettu :white_check_mark:
* HTTP Method: `POST`
* URL: `/v1/place/`
* Onnistuneen kutsun vastaus: `HTTP 201`
* Paluuarvo: luodun paika id

Esimerkki lähetettävästä datasta:
```JSON
{
 "latitude": 24.93876,
 "longitude": 60.17664,
 "name": "Kulmahuone"
}]
```

## Paikan päivitys

* Toteutuksen prioriteetti: 3
* Toteutuksen tila: ei toteutettu :white_check_mark:
* HTTP Method: `PUT`
* URL: `/v1/place/<aikan id>`
* Onnistuneen kutsun vastaus: `HTTP 200`

Esimerkki lähetettävästä datasta:
```JSON
{
 "latitude": 24.93876,
 "longitude": 60.17664,
 "name": "Kulmahuone"
}]
```

## Paikkojen listaus

* Toteutuksen prioriteetti: 3
* Toteutuksen tila: toteutettu :white_check_mark:
* HTTP Method: `GET`
* URL: `/v1/place/`
* Onnistuneen kutsun vastaus: `HTTP 200`

Esimerkkidata vastauksesta:
```JSON
[{
 "place_id": 1,
 "latitude": 24.93876,
 "longitude": 60.17664,
 "name": "Kulmahuone"
},
{
 "place_id": 2,
 "latitude": 24.93678,
 "longitude": 60.17499,
 "name": "Sivuhuone"
}]
```

## Kaikkien tilojen käyttöastetilasto

* Toteutuksen prioriteetti: 3
* Toteutuksen tila: ei toteutettu :x:
* HTTP Method:  `GET`
* URL: `/v1/query/usagestats`
* Query-parametrit:
  * `starting`: ajanhetki, josta lähtien käyttöaste lasketaan
  * `ending`: ajanhetki, johon asti käyttöaste lasketaan
  * `device_id` (prioriteetti 4): haluttu anturi, toistettavissa
  * `place_id` (prioriteetti 4): haluttu paikka, toistettavissa
    * jos `device_id` tai `place_id` annetaan useamman kerran, kaikki
      luetellut paikat ja anturit haetaan.  Jos kumpaakaan ei anneta,
      haetaan kaikki paikat ja anturit.
  * `type` (prioriteetti 4): haluttu mittaustyyppi, oletuksena "occupied"
* Onnistuneen kutsun vastaus: `HTTP 200`
* Laskee, mikä on halutun mittaustyypin arvojen keskiarvo halutuissa
  paikoissa / antureilla halutulla aikavälillä.  Kyllä/ei-arvoiset
  mittaukset tulkitaan kyllä=1 ja ei=0.

Esimerkkidata:
```JSON
{
 "type": "occupied",
 "average": 0.2
}
```

## Lähin vapaa tai vapautuva vessa

* Toteutuksen prioriteetti: 3
* Toteutuksen tila: ei toteutettu :x:
* HTTP Method: `GET`
* URL: `/v1/query/nearest`
* Query-parametrit:
  * `latitude`: tämänhetkisen sijainnin leveyspiiri (WGS84)
  * `longitude`: tämänhetkisen sijainnin pituuspiiri (WGS84)
* Onnistuneen kutsun vastaus: `HTTP 200`
* Laskee, missä on lähin vapaa vessa, tai jos se on hyvin kaukana, mikä
  lähellä olevista vessoista on todennäköisesti ensin vapautumassa
  (esim. on ollut jo pitkään käytössä).  Palauttaa kyseisen paikan
  tiedot kuten statuskyselyssä.

Esimerkkidata:
```JSON
{
 "place_id": 946,
 "latitude": 24.93866,
 "longitude": 60.17664,
 "occupied": false
}
```

## Muut sisältötyypit

* Prioriteetti: 5

Tiedot voi lähettää tai vastaanottaa myös CSV-muodossa käyttämällä
Content-type- ja Accept-otsakkeita.  Tällöin sanomassa ovat mukana samat
kentät kuin JSON-sanomassakin; rivi 1 kertoo kenttien nimet ja
järjestyksen.

Esimerkkidata (tapahtuman tallennus):
```CSV
"device_id","place_id","timestamp","type","value"
10123,945,"2016-04-10T12:49:12+22:45","obscured",true
```

Esimerkkidata (raakadatan haku):
```CSV
"device_id","place_id","timestamp","type","value"
10123,945,"2016-04-10T12:49:12+22:45","occupied",true
10456,945,"2016-03-10T12:49:12+22:45","ambient light",1030.07
```

Esimerkkidata (tämän hetken tilanne):
```CSV
"place_id","latitude","longitude","occupied"
945,24.93876,60.17664,true
946,24.93866,60.17664,false
```

