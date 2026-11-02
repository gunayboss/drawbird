# Translating DrawBird content

Source: `tools/i18n_content/tr.py` (Turkish). Target: `tools/i18n_content/<lang>.py`.

## Output shape

The target file defines the same six variables as the source, as plain Python literals, UTF-8:
`UI`, `LESSONS`, `BIRDS`, `PAGES`, `LEGAL`, `POSTS`.

- Same keys, same nesting, same list lengths, same order.
- Translate every string value. Keep `''` as `''`.
- Keep every `{placeholder}` exactly (you may move it inside the sentence).
- Keep every HTML tag in the same order, and every `href="..."` exactly as it is. Only translate the text between tags.
- Latin bird names are not translated. Turkish place names (Birecik, Tuz Gölü, Gediz Deltası, İstanbul Boğazı) stay, with the target-language word for lake/delta/strait if natural ("Lake Tuz", "the Bosphorus").
- Bird names: use the usual common name in the target language (Kumru → Eurasian collared dove, Leylek → white stork, Kelaynak → northern bald ibis …).
- Numbers and units stay metric; use the target language's decimal separator and number formatting.
- `UI['months']` = the 12 month names; `UI['date_format']` = a natural date pattern using `{d}`, `{month}`, `{y}`.
- `UI['tbl']` = the 6 table labels (size, wingspan, weight, diet, eggs, where to see it).
- The pages are about birds of Türkiye and a Turkish site; keep that context ("Birds of Türkiye"), do not localise it to the reader's country.
- `LEGAL['kvkk']` is the notice required by Turkish law (KVKK, law no. 6698). Translate it faithfully; keep "KVKK" and article numbers.

## Voice

Read `tools/YAZIM_TARZI.md`. Write like a friend talking: address the reader directly ("you" in the informal register where the language has one: tú, tu, du, ты, kamu …), short sentences, everyday words, a light joke where the Turkish has one. Natural native writing, not a word-for-word copy. No added facts, no invented personal experiences, nothing left out.

## Finish

Run `python -I tools/check_i18n.py <lang>` from the project root and fix every reported problem until it prints `<lang>: tamam`. Do not edit any other file.
If the file is long, write it in parts (for example UI + LESSONS first, then append BIRDS, PAGES, LEGAL, POSTS with edits) and run the check at the end.
