# DIY Diva

> Parte della collezione [Portable Diva](../README.md).

**Un avatar, tanti editor.** DIY Diva descrive il tuo personaggio ricorrente una volta sola, in modo
indipendente dai giochi, e lo traduce in una *ricetta* per l'editor di ciascun gioco: quali voci scegliere,
dove posizionare gli slider e quali colori usare.

## Perché una ricetta e non un file da importare

Quasi nessun gioco accetta avatar dall'esterno, e ogni editor ha un "vocabolario" diverso:

| Tipo di editor | Esempi | Strategia |
|---|---|---|
| **A scelte discrete** (liste numerate, preset) | Pokémon, Cyberpunk 2077, Diablo IV | si sceglie l'opzione più vicina al tratto canonico |
| **A slider** (valori continui) | Dragon Age: The Veilguard, Monster Hunter Wilds | il tratto 0–1 diventa una posizione dello slider |

La ricetta funziona sempre, anche a mano. Dove un gioco ha preset o codici condivisibili, in futuro un
adattatore potrà generarli direttamente.

## Come è fatto

```
schema/avatar.schema.json   descrizione canonica (JSON Schema, dà anche l'autocompletamento negli editor)
examples/                   un avatar d'esempio e le ricette generate per ogni gioco
verifiche/                  schede da compilare in gioco per confermare gli adattatori
adapters/<gioco>.json       come ogni editor traduce i tratti canonici
diy_diva/                   il motore (Python 3, nessuna dipendenza)
docs/                       note sul modello canonico e sui singoli giochi
```

### L'avatar canonico

- **Tratti continui** tra 0 e 1, dove 0.5 = media (`face.eye_size`, `face.jaw_width`, `body.height`, …).
- **Colori** in esadecimale (`#8b3a1e`); il motore li converte in CIELAB per confrontarli in modo percettivo.
- **Tratti discreti** con valori fissi (`hair.length`, `face.shape`, `facial_hair.style`, …).
- **Elenchi** di segni distintivi e accessori, e una lista di **stirpi preferite** per i giochi fantasy.

Ogni campo è facoltativo: ciò che non specifichi resta al valore predefinito del gioco.
Dettagli in [docs/modello.md](docs/modello.md).

## Uso

I comandi vanno lanciati dalla cartella `diy-diva/`.

```bash
python3 -m diy_diva giochi                                   # adattatori disponibili
python3 -m diy_diva valida examples/avatar-esempio.json      # controlla un avatar
python3 -m diy_diva ricetta examples/avatar-esempio.json --gioco dragon-age-veilguard
python3 -m diy_diva ricetta mio-avatar.json --gioco cyberpunk-2077 -o ricetta.md
python3 -m diy_diva verifica --gioco dragon-age-origins      # scheda di verifica da compilare in gioco
python3 -m unittest                                               # test
```

## Giochi supportati

| Serie | Adattatori | Tipo di editor |
|---|---|---|
| Pokémon | `pokemon-scarlatto-violetto`, `pokemon-legends-za` | scelte discrete |
| Dragon Age | `dragon-age-origins`, `dragon-age-2`, `dragon-age-inquisition`, `dragon-age-veilguard` | slider |
| Monster Hunter | `monster-hunter-world`, `monster-hunter-rise`, `monster-hunter-wilds` | slider + colori liberi |
| Monster Hunter Stories | `monster-hunter-stories`, `monster-hunter-stories-2` | scelte discrete |
| Cyberpunk 2077 | `cyberpunk-2077` | scelte discrete numerate |
| Diablo IV | `diablo-4` | scelte discrete |

Tutti gli adattatori sono **da verificare**: sono costruiti dalla documentazione pubblica degli editor,
quindi nomi delle voci, intervalli e cataloghi delle opzioni vanno confermati in gioco.
Vedi [docs/giochi.md](docs/giochi.md) per le note su ciascun editor.

## Verificare un gioco

1. Apri la scheda del gioco in [`verifiche/`](verifiche/) (oppure generala con `verifica --gioco <id>`).
2. Con l'editor del gioco aperto, spunta le voci che trovi e annota nome reale, intervallo e numero di opzioni.
3. Aggiungi le voci che mancano e segna quelle che non esistono. Le foto dei menu aiutano molto.
4. Con la scheda compilata si aggiorna l'adattatore e si segna `"verified": true`.

## Prossimi passi

1. Verificare gli adattatori in gioco e compilare i cataloghi (palette dei colori, varianti numerate).
2. Calibrare gli slider: misurare a che valore del gioco corrisponde la "media".
3. Generare direttamente preset/codici dove il gioco li supporta.
4. Più avanti: calibrazione automatica da screenshot (punti del volto misurati e confrontati con l'avatar).
