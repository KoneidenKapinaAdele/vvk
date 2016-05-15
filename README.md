# vvk

Vapaus, vessuus, karttuus - täydellinen reittiopas lähimpään vapaaseen
vessaan

## Mistä on kyse?

VVK on Adele-tiimin Koneiden Kapina 2016 -entry, jossa toteutetaan
laitteet ja palvelu lähimmän vapaan vessan (tai kokoustilan,
yhteiskäyttöisen tietokoneen, nukkumapaikan, sorvin, kahvitilan, ...)
löytämiseen ja käyttöaste-ennustuksiin perustuviin
käyttöaikasuosituksiin.

## Dokumentaatio

* Vaihe 1:
  * [POC-selaindemo](http://koneidenkapinaadele.github.io/vvk/)
  * [Muita kerättyjä toteutusideoita](muita-ideoita.md)
* Vaihe 2:
  * [Arkkitehtuuri](docs/arkkitehtuuri.md)
  * [Tietomalli](docs/tietomalli.md)
  * [Rajapinnat](docs/rajapinnat.md)
  * [Käyttöliittymä](http://koneidenkapinaadele.github.io/vvk-ui/)

## Lyhyt kuvaus palvelusta

vapaa vessa -kartta
- automaattisesti päivittyvä kartta siitä, mitkä vessat ovat vapaina
- onko Solitan vessojen ovissa jo kiihtyvyysantureita?
- tuottaa myös tilastotietoa esim. parhaista vessassakäyntiajoista.  Voidaan käyttää prediktiiviseen vessakäyttäytymiseen
- mahdollista brändätä suoraan on-demand-neukkarivaraukseen
- suositut ja vihatut tilat
- varoituksia normista poikkeaville (terveydellisistä tai konformistisista syistä)

## Hyviä ja huonoja puolia

- + ehkä helppo prototyypata toimistolla
- + tarve on jo olemassa
- + pääsee leikkimään datanlouhinnalla (ehkä)
- + helppo visualisoida, jolloin esittely kiva
- + laajennettavuus: pystyy tuottamaan uutta ja uutta hyödyllistä tietoa
- + laajennettavuus: pystyy soveltamaan hyvin monenlaisiin aiheisiin: onko tietty yhteiskäyttöinen resurssi vapaana, esim. sorvi, hitsauspaikka, laboratorio, tms
- - päällekkäisyys varausjärjestelmien kanssa
- - onko tarpeeksi hauska?

