# Arkkitehtuuri

Arkkitehtuuri koostuu kolmesta osasta:

1. Dataa keräävät anturit lähettävät tapahtumia pilvipalvelimelle HTTP POST-komennoilla.
2. Pilvipalvelin tallentaa anturien tapahtumat, hallitsee datan luonnin ja haun käyttöoikeuksia ja tarjoaa käyttöliittymälle valmiiksi pureskeltua dataa.
3. Selainkäyttöliittymä näyttää tietoa anturien datan perusteella

## Datan keräys antureilla
* Vastuuhenkilönä _Panu_
* Luultavasti sopivin mittaustapa on infrapunaan perustuva liiketunnistin
  * Solitan Thinklabin valmiit anturit eivät vastaa tähän tarpeeseen --> luultavasti ostettava uusia
* Isoin haaste on löytää tapa jolla anturin data saadaan työnnettyä pilvipalvelimelle talteen
  * Vaihtoehto 1: liiketunnistimessa on itsessään Wlan-liityntä
  * Vaihtoehto 2: liiketunnistin on kiinni tietokoneessa (USB tai Bluetooth), joka lähettää tiedot. Tietokone voi olla demossa kannettava tai esim. Rasberry Pi

## Pilvipalvelin
* Vastuuhenkilönä _Liisa_
* Stackinä relaatiotietokanta ja sovelluspalvelin
  * Tekniikoina Postgres ja Java Spring
* Alustana Heroku, joka tarjoaa helpoimman mahdollisen pipelinen
  * $16/kk saa Hobby-tason paketin, jossa on 10 miljoona riviä tietokantatilaa. Sillä voi lähteä liikkeelle.
* Pitää olla joku pääsynhallinta, jotta vain meidän liiketunistimet saa lisätä dataa ja vain Solitan käyttjät saa nähdä Solitan vessavaraustilanteen.
* Anturien datan tallentamiseen riittää yksi HTTP POST-rajapinta.
* Käyttöliittymällä on tarvetta monelle HTTP GET-rajapinnalle, jotka palauttaa valmiiksi käsiteltyä dataa, jotta käyttöliittymään ladattu datamäärä pysyy pienenä.
* Realiaikaisen varaustilanteen seurantaan olisi kiva kokeilla Push-notifikaatioita käyttöliittymälle Web Sockettien kautta.
* Pitää olla rajapinta kaiken raakadatan saamiseen analysointia varten.

## Selainkäyttöliittymä
* Vastuuhenkilö _Antti_
* Työpöydälle ja mobiiliin skaalautuva nettisivu
* Hakee datan Herokun pilvipalvelusta HTTP GET-kutsuilla.
* Vain staattisia resursseja, voidaan tarjota Githubin pagesin kautta tai Herokun pilvipalvelimelta.
* Ideoita käyttöliittymän ominaisuuksiksi:
  * _Kartta nykyisestä varaustilanteesta_: POC-demon mukainen kartta jossa näkyy käyttötilanne.
  * _Infotaulu/Radiaattori_: kahvitilaan/aulaan sopiva iso näyttö joka näyttää selkeillä väreillä kaikkien tilojen käyttötilanteen.
  * _Käyttötilanteen aikasarja_: kuvaaja, josta näkee kaikkien tai yhden tietyn tilan käyttö eri aikoina
  * _Varoitukset/ilmoitukset_: notifikaatio jos tilastollisesti tilan käyttöaste on tulevana ajanjaksona korkea
  * _Suunnistus_: etäisyys ja suunta lähimpään vapaaseen tilaan 
