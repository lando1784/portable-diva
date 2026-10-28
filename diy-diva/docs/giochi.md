# Note sui giochi

Riepilogo di come funziona ciascun editor e di cosa serve per rendere affidabile il suo adattatore.
Le informazioni vengono da guide e wiki pubbliche (fonti in fondo): **vanno verificate in gioco**, perché
le opzioni cambiano con patch e stagioni.

## Pokémon Scarlatto e Violetto

- **Tipo:** scelte discrete, con un buon editor del viso: forma degli occhi, lenti colorate, ciglia, sopracciglia,
  labbra, trucco e lentiggini, ognuno con il proprio colore.
- **Capelli:** 24 acconciature, 19 disponibili dall'inizio.
- **Da verificare:** se e come si sceglie la tonalità della pelle (sembra legata all'aspetto di partenza) e se si
  può cambiare dopo.

## Pokémon Leggende Z-A

- **Tipo:** solo scelte discrete. Non ci sono slider di forma: si parte da un aspetto di base, poi si scelgono
  tonalità della pelle, forma e colore degli occhi, ciglia, forma e colore delle sopracciglia, colore delle
  labbra, nei, lentiggini e occhiaie.
- **Capelli:** taglio e colore si cambiano al parrucchiere di Luminopoli e non sono legati al genere.
- **Attenzione:** alcune voci (la tonalità della pelle, secondo alcune fonti) potrebbero restare bloccate dopo la creazione.
- **Per l'avatar:** stile molto stilizzato, quindi la riconoscibilità passa da *colori + capelli + segni* più che
  dalla forma del viso.
- **Da fare:** catalogare la palette della pelle, i colori degli occhi e le acconciature.

## Dragon Age: Origins

- **Tipo:** a slider, senza numeri. Stirpe (umano, elfo, nano), sesso, preset del viso, poi slider raggruppati
  per zona: pelle, capelli, occhi, naso, bocca, mascella/guance, collo/orecchie, più ritratto e voce.
- **Attenzione:** le forme di un preset non sempre si combinano con un altro, alcuni slider possono "scattare"
  al massimo e c'è chi segnala che il colore degli occhi non cambia. L'editor del toolset ufficiale ha più
  opzioni di quello in gioco.
- **Da verificare:** i nomi reali degli slider per zona.

## Dragon Age II

- **Tipo:** a slider, evoluzione di Origins. Hawke è sempre umano e la voce è fissa per sesso.
- **Dopo la creazione:** lo specchio della trasformazione arriva con il DLC Emporio Nero.

## Dragon Age: Inquisition

- **Tipo:** a slider, senza coordinate. Stirpe (umano, elfo, nano, qunari), sesso, preset e molti slider,
  compresi barba, guance e corna per i qunari.
- **Attenzione:** l'illuminazione dell'editor è scura e verdastra, quindi i colori in gioco appaiono diversi.
- **Dopo la creazione:** specchio all'Emporio Nero (DLC gratuito).

## Dragon Age: The Veilguard

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

## Monster Hunter: World

- **Tipo:** preset, poi liste di forme (tipo di viso, naso, bocca, circa 20 varianti ciascuna) affinate da slider
  (posizione di occhi, naso e bocca, apertura degli occhi, lunghezza delle ciglia), più palette dettagliate per
  i colori.
- **Dopo la creazione:** acconciatura e trucco si cambiano in camera; per viso, pelle e corpo serve un buono
  modifica personaggio.
- **Da verificare:** alcuni salvataggi della community riportano valori numerici, quindi gli slider potrebbero
  avere un intervallo preciso: in tal caso si passa da percentuali a numeri esatti.

## Monster Hunter Rise

- **Tipo:** struttura simile a World, con tre livelli di trucco indipendenti (tipo, posizione, dimensione,
  colore), ottimi per pitture e segni.
- **Dopo la creazione:** l'aspetto si cambia dal baule fuori dalle missioni; viso e corpo richiedono un buono.

## Monster Hunter Stories 1 e 2

- **Tipo:** scelte discrete in stile chibi. In Stories 2: forma del viso, pelle, trucco, voce e acconciature
  con due colori in posizioni prefissate.
- **Dopo la creazione (Stories 2):** solo acconciatura, trucco e abiti, quindi viso, pelle e voce vanno scelti
  subito.
- **Da verificare:** le opzioni di Stories 1 (le fonti trovate sono scarse).

## Monster Hunter Wilds

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
- Pokémon Scarlatto/Violetto: [GGRecon](https://www.ggrecon.com/guides/pokemon-scarlet-and-violet-character-customisation/),
  [Nintendo Wire](https://nintendowire.com/news/2022/08/03/pokemon-scarlet-and-violet-further-details-character-customization)
- Dragon Age: Origins: [GameBanshee](https://gamebanshee.com/kwhaf),
  [datoolset.net – Morph](https://datoolset.net/wiki/Morph), [Nexus Mods](https://www.nexusmods.com/dragonage/mods/650)
- Dragon Age II: [Nexus Mods – Character Creator Guide](https://www.nexusmods.com/dragonage2/articles/21)
- Dragon Age: Inquisition: [RPG Site](https://rpgsite.net/news/3917-dragon-age-inquistion-shows-off-its-character-creator),
  [PC Gamer](https://www.pcgamer.com/show-us-your-inquisitor/)
- Monster Hunter: World: [Gematsu](https://gematsu.com/2017/09/monster-hunter-world-tgs-2017-special-stage-character-palico-creation),
  [Destructoid](https://www.destructoid.com/?p=222795)
- Monster Hunter Rise: [Shacknews](https://shacknews.com/article/123413/how-to-change-your-appearance-monster-hunter-rise),
  [Samurai Gamers](https://samurai-gamers.com/monster-hunter-rise/character-customization-2/)
- Monster Hunter Stories 2: [RPG Site](https://www.rpgsite.net/news/10284-monster-hunter-stories-2-will-let-you-customize-the-protagonist),
  [Siliconera](https://siliconera.com/monster-hunter-stories-2-character-creator)
- Monster Hunter Wilds: [Automaton](https://automaton-media.com/en/news/monster-hunter-wilds-character-creator-is-being-used-to-make-scarily-accurate-recreations-of-superheroes-actors-and-characters-from-other-games/),
  [Icy Veins](https://wp-prod.icy-veins.com/save-your-beta-look-transfer-designs-to-monster-hunter-wilds/)
