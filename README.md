# Portable Diva

**Un avatar, tanti editor.** Portable Diva descrive il tuo personaggio ricorrente una volta sola, in modo
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
adapters/<gioco>.json       come ogni editor traduce i tratti canonici
portable_diva/              il motore (Python 3, nessuna dipendenza)
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

```bash
python3 -m portable_diva giochi                                   # adattatori disponibili
python3 -m portable_diva valida examples/avatar-esempio.json      # controlla un avatar
python3 -m portable_diva ricetta examples/avatar-esempio.json --gioco dragon-age-veilguard
python3 -m portable_diva ricetta mio-avatar.json --gioco cyberpunk-2077 -o ricetta.md
python3 -m unittest                                               # test
```

## Giochi supportati (v0.1)

| Adattatore | Gioco | Stato |
|---|---|---|
| `pokemon-legends-za` | Pokémon Leggende Z-A (e Scarlatto/Violetto) | da verificare |
| `dragon-age-veilguard` | Dragon Age: The Veilguard (logica simile a Inquisition) | da verificare |
| `cyberpunk-2077` | Cyberpunk 2077 | da verificare |
| `diablo-4` | Diablo IV | da verificare |
| `monster-hunter-wilds` | Monster Hunter Wilds (logica simile a World/Rise) | da verificare |

"Da verificare" significa che gli adattatori sono costruiti dalla documentazione pubblica degli editor:
i nomi delle voci, gli intervalli e i cataloghi delle opzioni vanno confermati in gioco.
Vedi [docs/giochi.md](docs/giochi.md) per le note su ciascun editor e su come completarne il catalogo.

## Prossimi passi

1. Verificare gli adattatori in gioco e compilare i cataloghi (palette dei colori, varianti numerate).
2. Calibrare gli slider: misurare a che valore del gioco corrisponde la "media".
3. Generare direttamente preset/codici dove il gioco li supporta.
4. Più avanti: calibrazione automatica da screenshot (punti del volto misurati e confrontati con l'avatar).
