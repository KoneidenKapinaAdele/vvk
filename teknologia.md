---
layout: default
---

### Palvelun tekninen rakenne

![arkkitehtuurikaavio](images/arkkitehtuuri.png)

[Tekninen
arkkitehtuuri](https://github.com/KoneidenKapinaAdele/vvk/blob/master/docs/arkkitehtuuri.md)
on kuvattu myös projektin Github-sivuilla.

Arkkitehtuuri koostuu neljästä osasta:

1. Dataa keräävät anturit lähettävät tapahtumia pilvipalvelimelle HTTP
   POST-komennoilla.
2. Pilvipalvelin tallentaa anturien tapahtumat, hallitsee datan luonnin
   ja haun käyttöoikeuksia ja tarjoaa käyttöliittymälle valmiiksi
   pureskeltua dataa.
3. Selainkäyttöliittymä näyttää tietoa anturien datan perusteella
4. Datan analyysi pureksii raakadataa ja löytää uusia, yllättäviä
   asioita

### Tiedonkeruun toteutus

Tilojen varaustilannetta seurataan yhdistelemällä tietoa liikeantureista
ja oven aukioloa seuraavista antureista.  Mikäli tilassa on ollut
liikettä, se pysyy varattuna niin kauan, kuin ovi on kiinni.

![antureita ja tukiasema](images/anturit.jpeg)

