# legifouille

Pour fouiller la base LEGI https://echanges.dila.gouv.fr/OPENDATA/LEGI/

## `update_legi.sh` 

Script bash qui télécharge et décompresse la base LEGI dans le dossier local LEGI, puis en fabrique une archive `fr-legi-code-en-vigueur.tar.gz`.

## `update_data.sh`

Script bash qui utilise `legifouille.py` pour récupérer dans la base LEGI locale toutes les versions de tous les articles des codes mentionnés dans `data/fr-legi-codes-en-vigueur.csv`

En sortie, on obtient `fr-legi-codes-en-vigueur-versions.csv` et `fr-legi-codes-en-vigueur-liens.csv` (et les `.err` associés).

## `legifouille.Rmd` / `legifouille.md` 

Chargement naïf des données et affichage de statistiques foireuses sur tous les codes.

## `legifouille-code.Rmd` / `legifouille-md.md` 

Retravail plus en profondeur des données, ciblé sur un seul code à la fois (le code de l'éducation pour l'instant), pour produire des statistiques plus solides et des waffles. 

