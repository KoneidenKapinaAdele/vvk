# Rajapinnat

## Uuden tapahtuman tallennus

HTTP Metdod: `POST`
URL: `/event`
Onnistuneen tapahtuman luonin vastaus: `HTTP 201`

Esimerkkidata:
```
{
	"device_id" : 10123
	"event_datetime" : "2016-04-10T12:49:12+22:45"
	"occupied" : true
}
```

## Tämän hetken kaikkien anturien käyttötilanteen selvitys

HTTP Metdod: `GET`
URL: `/status/current`
Onnistuneen kutsun vastaus: `HTTP 200`

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