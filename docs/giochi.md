# Note sui giochi

Riepilogo di come funziona ciascun editor e di cosa serve per rendere affidabile il suo adattatore.
Le informazioni vengono da guide e wiki pubbliche (fonti in fondo): **vanno verificate in gioco**, perché
le opzioni cambiano con patch e stagioni.

## Pokémon Leggende Z-A (e Scarlatto/Violetto)

- **Tipo:** solo scelte discrete. Non ci sono slider di forma: si parte da un aspetto di base, poi si scelgono
  tonalità della pelle, forma e colore degli occhi, ciglia, forma e colore delle sopracciglia, colore delle
  labbra, nei, lentiggini e occhiaie.
- **Capelli:** taglio e colore si cambiano al parrucchiere di Luminopoli e non sono legati al genere.
- **Attenzione:** alcune voci (la tonalità della pelle, secondo alcune fonti) potrebbero restare bloccate dopo la creazione.
- **Per l'avatar:** stile molto stilizzato, quindi la riconoscibilità passa da *colori + capelli + segni* più che
  dalla forma del viso.
- **Da fare:** catalogare la palette della pelle, i colori degli occhi e le acconciature.

## Dragon Age: The Veilguard (e Inquisition)

- **Tipo:** a slider, il più ricco della lista. Si sceglie la stirpe (umano, elfo, nano, qunari), poi il viso
  come miscela di tre preset e si affina con slider per zona: fronte, sopracciglia, occhi, naso, zigomi, bocca,
  mascella, mento.
- **Corpo:** controllo "a triangolo" tra magro, muscoloso e robusto, più gli slider di altezza e peso.
  Corrisponde direttamente a `body.build`.
- **Pelle:** slider per melanina e vitiligine, che l'adattatore ricava dal colore della pelle e da `skin.vitiligo`.
- **Dopo la creazione:** si può modificare tutto allo Specchio della trasformazione.
- **Da fare:** verificare i nomi esatti degli slider e controllare che il centro corrisponda davvero alla media.
  Per Inquisition serve un adattatore a parte, con la stessa logica.

## Cyberpunk 2077

- **Tipo:** scelte discrete numerate. Naso, bocca e mascella hanno 22 varianti ciascuno, e anche occhi,
  sopracciglia, orecchie, acconciature e colori sono liste.
- **Separati:** il tipo di corpo e il tono di voce si scelgono indipendentemente.
- **Extra:** cicatrici, tatuaggi, piercing e cyberware sul viso, che corrispondono bene a `marks`.
- **Da fare:** il lavoro più utile è dare un `match` a ciascuna delle 22 varianti di naso, bocca e mascella.
  Dopo averlo fatto, la ricetta indica il numero esatto.

## Diablo IV

- **Tipo:** scelte discrete, legate alla classe. Ogni classe ha i suoi preset e la corporatura è fissata dalla
  classe, quindi conta solo il viso.
- **Opzioni (circa, al lancio):** 11 acconciature, 11 barbe, circa 30 colori di capelli e circa 30 tonalità
  di pelle, 12 colori degli occhi, 14 trucchi, oltre a segni e gioielli.
- **Dopo la creazione:** viso e pelle restano fissi; segni e gioielli si cambiano.
- **Da fare:** cataloghi per classe (preset e acconciature cambiano da una classe all'altra).

## Monster Hunter Wilds (e World/Rise)

- **Tipo:** a slider, molto dettagliato, con selettori di colore liberi: i colori dell'avatar si possono
  riprodurre quasi esattamente.
- **Condivisione:** la community si scambia i personaggi tramite codici. Se il formato si dimostra stabile,
  potrebbe diventare il primo vero "import" del progetto.
- **Da fare:** confermare le voci degli slider e il loro intervallo, poi capire come funzionano i codici.

## Fonti

- Pokémon Leggende Z-A: [Serebii – Looks](https://www.serebii.net/legendsz-a/looks.shtml),
  [Insider Gaming](https://insider-gaming.com/pokemon-legends-z-a-character-customization-explained/),
  [Siliconera](https://www.siliconera.com/how-to-change-pokemon-legends-z-a-clothes-and-glasses/),
  [Dexerto](https://www.dexerto.com/wikis/pokemon-legends-z-a/change-appearance-outfit-all-outfits)
- Dragon Age: The Veilguard: [EA – Character creator](https://www.ea.com/en-au/games/dragon-age/dragon-age-the-veilguard/character-creator),
  [Fextralife](https://dragonageveilguard.wiki.fextralife.com/Character+Creation),
  [GamingBolt](https://gamingbolt.com/dragon-age-the-veilguard-character-creator-complexions-qunari-horn-materials-and-more-detailed),
  [PC Gamer](https://pcgamer.com/games/dragon-age/veilguard-change-appearance)
- Cyberpunk 2077: [Fandom – Character Customization](https://cyberpunk.fandom.com/wiki/Cyberpunk_2077_Character_Customization),
  [PC Gamer](https://pcgamer.com/cyberpunk-2077-character-customization-creation)
- Diablo IV: [Maxroll](https://maxroll.gg/d4/getting-started/character-customization),
  [PureDiablo](https://www.purediablo.com/diablo4/Character_Customization),
  [PC Gamer](https://pcgamer.com/diablo-4-character-creation)
- Monster Hunter Wilds: [Automaton](https://automaton-media.com/en/news/monster-hunter-wilds-character-creator-is-being-used-to-make-scarily-accurate-recreations-of-superheroes-actors-and-characters-from-other-games/),
  [Icy Veins](https://wp-prod.icy-veins.com/save-your-beta-look-transfer-designs-to-monster-hunter-wilds/)
