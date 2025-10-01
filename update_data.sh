python3 legifouille.py data/fr-legi-codes-en-vigueur.csv > data/fr-legi-codes-en-vigueur-versions.csv 2> data/fr-legi-codes-en-vigueur-versions.err
python3 legifouille.py --liens data/fr-legi-codes-en-vigueur.csv > data/fr-legi-codes-en-vigueur-liens.csv 2> data/fr-legi-codes-en-vigueur-liens.err

tar -czf fr-legi-code-en-vigueur.tar.gz data

echo "Errors versions: `wc -l data/fr-legi-codes-en-vigueur-versions.err`"
echo "Errors liens: `wc -l data/fr-legi-codes-en-vigueur-liens.err`"
