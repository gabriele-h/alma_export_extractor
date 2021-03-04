## Verwendung

```bash
python xml_extractor.py input.xml output.csv 100,77308w,77308v
```

### Alle Subfelder
Wenn keine Subfelder angegeben werden, werden alle Subfelder präfigiert mit
"$$<subfeld-code>" und in einer Zelle zusammen gehängt ausgegeben. Dabei können
Indikatoren weggelassen, angegeben oder durch Asteriske ersetzt werden.

```bash
python xml_extractor.py input.xml output.csv 100,245**, 77308
```

### Bestimmte Subfelder ohne bestimmte Indikatoren
Wenn Indikatoren irrelevant sind, müssen beide(!) durch Asteriske ersetzt
werden:

```bash
python xml_extractor.py input.xml output.csv 245**a,245**b
```

Wichtig ist, dass bei der Angabe der Kategorien keine Leerzeichen enthalten sind.

## Column splitter

Wenn gewünscht ist, dass die Mehrfachvorkommen zusätzlich in eigene Spalten
aufgedröselt werden, kann der column_splitter verwendet werden.

```bash
python column\_splitter.py input.csv output.csv
```

Pro Spalte wird geschaut, wie oft der Delimiter '---' vorkommt. Auf Basis davon
wird ein neues CSV generiert, das eine Spalte mit " gesamt" Suffix hat und darauf
folgend die Spalten, in denen die gesplitteten Inhalte gelistet und ein numerisches
Suffix hochgezählt wird (z. B. "(1)").

Der Delimiter steht jeweils hardcoded in den Dateien drin.