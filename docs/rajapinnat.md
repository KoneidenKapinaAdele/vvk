# Rajapinnat

## Uuden tapahtuman tallennus

* Toteutuksen prioriteetti: 1
* HTTP Metdod: `POST`
* URL: `/event`
* Onnistuneen tapahtuman luonin vastaus: `HTTP 201`

Esimerkkidata:
```
{
	"device_id" : 10123
	"event_datetime" : "2016-04-10T12:49:12+22:45"
	"occupied" : true
}
```

## Tapahtumien raakadatan haku

* Toteutuksen prioriteetti: 1
* HTTP Metdod: `GET`
* URL: `/event/`
* Onnistuneen kutsun vastaus: `HTTP 200`

Esimerkkidata:
```
{
	events: [
		{
			"device_id" : 10123
			"event_datetime" : "2016-04-10T12:49:12+22:45"
			"occupied" : true
		},
		{
			"device_id" : 10456
			"event_datetime" : "2016-03-10T12:49:12+22:45"
			"occupied" : false
		}
	]
}
```

## Tämän hetken kaikkien anturien käyttötilanteen selvitys

* Toteutuksen prioriteetti: 1
* HTTP Metdod: `GET`
* URL: `/status/current`
* Onnistuneen kutsun vastaus: `HTTP 200`

Esimerkkidata:
```
{
	status: [
		{
			"device_id" : 10123
			"occupied" : true
		},
		{
			"device_id" : 10456
			"occupied" : false
		}
	]
}
```

## Kaikkien tilojen käyttötilanteen historian aikasarja päivämäärälle

* Toteutuksen prioriteetti: 2
* HTTP Metdod: `GET`
* URL: `/status/timeserie/<ISO date>`, esim. `/status/timeserie/2016-04-27`
* Onnistuneen kutsun vastaus: `HTTP 200`
* Selite: kaikkien anturien datasta lasketut aikasarja parametrina annettulle päivälle. Aikasarjassa on käyttöaste, eli kuinka monta prosenttia kustakin tunnista tilat ovat olleet varattuna.

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
* HTTP Metdod: `GET`
* URL: `/status/device/<device id>/timeserie/<ISO date>`, esim. `/status/device/10456/timeserie/2016-04-27`
* Onnistuneen kutsun vastaus: `HTTP 200`
* Selite: tietyn anturin datasta lasketut aikasarja parametrina annettulle päivälle. Aikasarjassa on käyttöaste, eli kuinka monta prosenttia kustakin tunnista tila on ollut varattuna.

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