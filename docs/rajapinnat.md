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
 "event_datetime": "2016-04-10T12:49:12+22:45",
 "type": "obscured",
 "value": true
}
```

* `event_datetime`-kenttä on valinnainen.
* `type`-kentän arvoja ovat ainakin: "occupied", "ambient light",
  "movement", "obscured"
  * "occupied" on tarkoitettu antureille, jotka haluavat itse päätellä,
    onko paikassa joku.  Muut parametrit ovat antureiden raakadataa.

## Tapahtumien raakadatan haku

* Toteutuksen prioriteetti: 1
* HTTP Method: `GET`
* URL: `/v1/event/`
* Query-parametrit:
  * `not_before`: oletusarvo äärettömän kaukana menneisyydessä
  * `not_after`: oletusarvo äärettömän kaukana tulevaisuudessa
  * `device_id`: haluttu anturi, oletuksena kaikki, toistettavissa
  * `place_id`: haluttu paikka, oletuksena kaikki, toistettavissa
  * `type`: haluttu mittaustyyppi, oletuksena kaikki, toistettavissa
* Onnistuneen kutsun vastaus: `HTTP 200`

Esimerkkidata:
```
[{
 "device_id": 10123,
 "place_id": 945,
 "event_datetime": "2016-04-10T12:49:12+22:45",
 "type": "occupied",
 "value": true
}, {
 "device_id": 10456,
 "place_id": 945,
 "event_datetime": "2016-03-10T12:49:12+22:45",
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
 "device_id": 10123,
 "place_id": 945,
 "occupied": true
}, {
 "device_id": 10456,
 "place_id": 945,
 "occupied": false
}]
```

## Kaikkien tilojen käyttötilanteen historian aikasarja päivämäärälle

* Toteutuksen prioriteetti: 2
* HTTP Method: `GET`
* URL: `/v1/status/timeserie/<ISO date>`, esim. `/status/timeserie/2016-04-27`
* Onnistuneen kutsun vastaus: `HTTP 200`
* Selite: kaikkien anturien datasta lasketut aikasarja parametrina
  annettulle päivälle. Aikasarjassa on käyttöaste, eli kuinka monta
  prosenttia kustakin tunnista tilat ovat olleet varattuna.

Esimerkkidata:
```
{
	timeserie: [
		{
			"hour" : 1
			"occupied_percentage" : 0
		},
		{
			"hour" : 7
			"occupied_percentage" : 20
		},
		{
			"hour" : 12
			"occupied_percentage" : 90
		}
	]
}
```

## Tietyn tilan käyttötilanteen historian aikasarja päivämäärälle

* Toteutuksen prioriteetti: 3
* HTTP Method: `GET`
* URL: `/v1/status/device/<device id>/timeserie/<ISO date>`, esim.
  `/status/device/10456/timeserie/2016-04-27`
* Onnistuneen kutsun vastaus: `HTTP 200`
* Selite: tietyn anturin datasta lasketut aikasarja parametrina
  annettulle päivälle. Aikasarjassa on käyttöaste, eli kuinka monta
  prosenttia kustakin tunnista tila on ollut varattuna.

Esimerkkidata:
```
{
	timeserie: [
		{
			"hour" : 1
			"occupied_percentage" : 0
		},
		{
			"hour" : 7
			"occupied_percentage" : 20
		},
		{
			"hour" : 12
			"occupied_percentage" : 90
		}
	]
}
```
