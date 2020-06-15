# Metalib XML Extractor
Verwandelt Informationen aus den Knowledge Units in TSV-Format.

## Notwendige Datenvorbereitungen

```vi
:%s/<line>.*<\/line>//
```

Das ist deshalb notwendig, weil in konkret diesen Zeilen das Encoding
kaputt ist und das XML sonst nicht geparst werden kann.

## Verwendung

python xml_extractor.py input.xml output.tsv