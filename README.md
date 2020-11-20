## Verwendung

python xml\_extractor.py input.xml output.csv 100,77308w,77308v

### Alle Subfelder
Wenn keine Subfelder angegeben werden, werden alle Subfelder präfigiert mit
"$$<subfeld-code>" und in einer Zelle zusammen gehängt ausgegeben. Dabei können
Indikatoren weggelassen, angegeben oder durch Asteriske ersetzt werden.

python xml\_extractor.py input.xml output.csv 100,245\*\*, 77308

### Bestimmte Subfelder ohne bestimmte Indikatoren
Wenn Indikatoren irrelevant sind, müssen beide(!) durch Asteriske ersetzt
werden:

python xml\_extractor.py input.xml output.csv 245\*\*a,245\*\*b

Wichtig ist, dass bei der Angabe der Kategorien keine Leerzeichen enthalten sind.
