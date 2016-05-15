# Tietomalli

## Tapahtumat

Kenttä | Tyyppi | Esimerkki | Selite
-------|--------|-----------|----------
device_id | integer | `100` | Anturin yksilöllinen tunniste
place_id | integer | `300` | Paikan/huoneen yksilöllinen tunniste
timestamp | datetime | `2016-05-13T13:44:32+00:00` | Tapahtuman tapahtumisajanhetki
measurement_type | enum | `movement` | Millainen mittaus on kyseessä
measurement_value | decimal | `2.0` | Mittauksen tulos, vaihteluväli riippuu mittaustyypistä

## Paikat

Kenttä | Tyyppi | Esimerkki | Selite
-------|--------|-----------|----------
place_id | integer | `300` | Paikan/huoneen yksilöllinen tunniste
latitude | decimal | `25.09` | Paikan leveyspiiri WGS84-koordinaatteina
longitude | decimal | `63.057` | Paikan pituuspiiri WGS84-koordinaatteina

