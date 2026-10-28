# Il modello canonico

Il file avatar descrive *chi è* il personaggio, non *come lo costruisce* un certo gioco.
Le regole di base sono queste.

1. **Semantico, non tecnico.** "Occhi grandi" (`face.eye_size: 0.7`) e non "slider 3 dell'editor X a 62".
2. **0.5 è la media.** Ogni tratto continuo va da 0 a 1. Lo 0.5 è il "volto medio" che
   quasi tutti gli editor mettono al centro degli slider. Per le quantità (lentiggini, trucco, vitiligine),
   0 significa "assente".
3. **Tutto è facoltativo.** Un tratto mancante lascia il valore predefinito del gioco.
4. **I colori sono percettivi.** Si scrivono in esadecimale. Il motore li confronta in CIELAB, così il
   "castano ramato" scelto dalla palette di un gioco è quello che *sembra* più vicino, non quello
   numericamente più vicino in RGB.

## Campi

| Gruppo | Campi | Note |
|---|---|---|
| `identity` | `presentation`, `apparent_age`, `lineage_preference` | `presentation`: 0 maschile, 1 femminile. `lineage_preference` è un elenco ordinato (`["elf", "human"]`): ogni gioco sceglie la prima stirpe che ha. |
| `body` | `height`, `weight`, `build` | `build` è un insieme di pesi (`lean`, `muscular`, `heavy`) che il motore normalizza, adatto ai controlli "a triangolo". |
| `skin` | `color`, `undertone`, `freckles`, `vitiligo`, `dark_circles`, `beauty_marks` | |
| `face` | `shape`, `face_length`, `forehead_height`, `brow_height`, `brow_thickness`, `eye_size`, `eye_spacing`, `eye_tilt`, `nose_width`, `nose_length`, `nose_bridge`, `cheekbone_prominence`, `cheek_fullness`, `lip_fullness`, `mouth_width`, `jaw_width`, `chin_prominence`, `ear_size` | `shape` è uno tra `oval`, `round`, `square`, `heart`, `long`, `diamond`. |
| `eyes` | `color`, `secondary_color` | `secondary_color` per l'eterocromia. |
| `brows` | `color` | Se manca, gli adattatori usano il colore dei capelli. |
| `hair` | `length`, `texture`, `style_tags`, `bangs`, `color`, `highlight_color` | `style_tags` è libero (`ponytail`, `undercut`, `braid`, …) e serve per scegliere l'acconciatura più simile. |
| `facial_hair` | `style`, `color` | |
| `makeup` | `eyeliner`, `blush`, `lip_color` | |
| `voice` | `pitch` | 0 grave, 1 acuto. |
| `marks` | elenco di `{type, area, description}` | `type`: `scar`, `tattoo`, `paint`, `cyberware`, `piercing`, `other`. |
| `accessories` | elenco di `{type, description}` | |
| `notes` | testo libero | |

Lo schema formale è in [`schema/avatar.schema.json`](../schema/avatar.schema.json). Se il tuo editor di testo
supporta JSON Schema (VS Code lo fa), la riga `"$schema"` nel file avatar attiva l'autocompletamento.

## Gli adattatori

Un adattatore (`adapters/<gioco>.json`) elenca le voci dell'editor, raggruppate in sezioni come nel gioco.
Ogni voce ha un `type`:

| Tipo | Cosa fa | Campi |
|---|---|---|
| `slider` | trasforma un tratto 0–1 in una posizione | `from`; facoltativi `min`/`max`/`step` (altrimenti la posizione è in % della corsa), `invert`, `transform` (`darkness`: dal colore della pelle ricava quanto è scura, per gli slider "melanina") |
| `choice` | sceglie un'opzione | `options` con `match` (tratti di riferimento di ciascuna opzione), oppure `hint` (tratti da descrivere quando il catalogo non è ancora compilato) e `count` |
| `color` | indica il colore | `from`; facoltativa `palette` (`[{value, hex}]`): se c'è, sceglie il campione più vicino |
| `toggle` | sì/no | `from`, `threshold` |
| `weights` | miscela di corporature | `from: "body.build"`, `labels` |
| `list` | riporta segni o accessori | `from`, `types` |
| `note` | consiglio fisso | `text` |

`from` può essere un elenco di percorsi: si usa il primo presente (es. `["brows.color", "hair.color"]`).

### Compilare un catalogo

Il modo più rapido per migliorare un adattatore è descrivere le opzioni di una voce `choice`. Per esempio,
dopo aver guardato i 22 nasi di Cyberpunk:

```json
{"label": "Naso", "type": "choice", "options": [
  {"value": "Naso 1",  "match": {"face.nose_width": 0.5, "face.nose_length": 0.5}},
  {"value": "Naso 2",  "match": {"face.nose_width": 0.2, "face.nose_length": 0.6}},
  ...
]}
```

e lo stesso vale per le palette:

```json
{"label": "Colore dei capelli", "type": "color", "from": "hair.color", "palette": [
  {"value": "Colore 1", "hex": "#1b1b1b"},
  {"value": "Colore 2", "hex": "#5a3a22"}
]}
```
