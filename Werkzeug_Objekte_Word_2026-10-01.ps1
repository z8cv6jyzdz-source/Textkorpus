# Werkzeug_Objekte_Word_2026-10-01.ps1 - Word-Vorlage der Objekte in Word oeffnen, Felder in der richtigen
# Reihenfolge aktualisieren (erst SEQ, dann Verzeichnisse), als .docx und .pdf speichern.
# Bachelorarbeit U15-Plyometrie, Setzwerkzeug zu Werkzeug_Objekte_Docx_2026-10-01.py, kein Manuskripttext.
# Aufruf: powershell -ExecutionPolicy Bypass -File Werkzeug_Objekte_Word_2026-10-01.ps1 <roh.docx> <ziel.docx> <ziel.pdf>
param([string]$Roh, [string]$Ziel, [string]$Pdf)
$ErrorActionPreference = 'Stop'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
  $doc = $word.Documents.Open($Roh, $false, $false, $false)
  # Reihenfolge: zuerst alle SEQ-Felder (Typ 12), dann Verzeichnisse (TablesOfFigures, TablesOfContents).
  # Ein schlichtes Fields.Update() baut die Verzeichnisse am Dokumentanfang vor den SEQ-Feldern (Befund 01.10.).
  foreach ($f in $doc.Fields) { if ($f.Type -eq 12) { [void]$f.Update() } }
  foreach ($t in $doc.TablesOfFigures) { [void]$t.Update() }
  foreach ($t in $doc.TablesOfContents) { [void]$t.Update() }
  "TablesOfFigures: " + $doc.TablesOfFigures.Count + " / TablesOfContents: " + $doc.TablesOfContents.Count
  $doc.Repaginate()
  $doc.SaveAs2($Ziel, 16)
  $doc.ExportAsFixedFormat($Pdf, 17)
  "Seiten: " + $doc.ComputeStatistics(2)
  "Tabellen: " + $doc.Tables.Count
  "Felder: " + $doc.Fields.Count
  $doc.Close(0)
} finally {
  $word.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
