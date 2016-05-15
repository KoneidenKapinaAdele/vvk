# Rajapinnat

## Uuden tapahtuman tallennus

* Toteutuksen prioriteetti: 1
* HTTP Method: `POST`
* URL: `/v1/event`
* Onnistuneen tapahtuman luonin vastaus: `HTTP 201`

Esimerkkidata:
```
{
 "device_id": 10123,
 "place_id": 945,
 "timestamp": "2016-04-10T12:49:12+22:45",
 "type": "obscured",
 "value": true
}
```

* `timestamp`-kenttä on valinnainen.  Oletusarvo vastaanottohetki.
* `type`-kentän arvoja ovat ainakin: "occupied", "ambient light",
  "movement", "obscured"
  * "occupied" on tarkoitettu antureille, jotka haluavat itse päätellä,
    onko paikassa joku.  Muut parametrit ovat antureiden raakadataa.

## Tapahtumien raakadatan haku

* Toteutuksen prioriteetti: 1
* HTTP Method: `GET`
* URL: `/v1/event/`
* Query-parametrit:
  * `starting`: jättää pois tätä aiemmat tapahtumat, oletusarvo
    äärettömän kaukana menneisyydessä
  * `ending`: jättää pois tätä myöhemmät tapahtumat, oletusarvo
    äärettömän kaukana tulevaisuudessa
  * `device_id`: haluttu anturi, toistettavissa
  * `place_id`: haluttu paikka, toistettavissa
    * jos `device_id` tai `place_id` annetaan useamman kerran, kaikki
      luetellut paikat ja anturit haetaan.  Jos kumpaakaan ei anneta,
      haetaan kaikki paikat ja anturit.
  * `type`: haluttu mittaustyyppi, oletuksena kaikki, toistettavissa
* Onnistuneen kutsun vastaus: `HTTP 200`

Esimerkkidata:
```
[{
 "device_id": 10123,
 "place_id": 945,
 "timestamp": "2016-04-10T12:49:12+22:45",
 "type": "occupied",
 "value": true
}, {
 "device_id": 10456,
 "place_id": 945,
 "timestamp": "2016-03-10T12:49:12+22:45",
 "type": "ambient light",
 "value": 1030.07
}]
```

## Kaikkien anturien tämän hetken tilanteen selvitys

* Toteutuksen prioriteetti: 1
* HTTP Method: `GET`
* URL: `/v1/status/current`
* Onnistuneen kutsun vastaus: `HTTP 200`

Esimerkkidata:
```
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

## Kaikkien tilojen käyttöastetilasto

* Toteutuksen prioriteetti: 2
* HTTP Method: `GET`
* URL: `/v1/status/usage`
* Query-parametrit:
  * `starting`: ajanhetki, josta lähtien käyttöaste lasketaan
  * `ending`: ajanhetki, johon asti käyttöaste lasketaan
  * `device_id`: haluttu anturi, toistettavissa
  * `place_id`: haluttu paikka, toistettavissa
    * jos `device_id` tai `place_id` annetaan useamman kerran, kaikki
      luetellut paikat ja anturit haetaan.  Jos kumpaakaan ei anneta,
      haetaan kaikki paikat ja anturit.
  * `type`: haluttu mittaustyyppi, oletuksena "occupied"
* Onnistuneen kutsun vastaus: `HTTP 200`
* Laskee, mikä on halutun mittaustyypin arvojen keskiarvo halutuissa
  paikoissa / antureilla halutulla aikavälillä.  Kyllä/ei-arvoiset
  mittaukset tulkitaan kyllä=1 ja ei=0.

Esimerkkidata:
```
{
 "type": "occupied",
 "average": 0.2
}

## Lähin vapaa tai vapautuva vessa

* Toteutuksen prioriteetti: 2
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
```
{
 "place_id": 946,
 "latitude": 24.93866,
 "longitude": 60.17664,
 "occupied": false
}
```

