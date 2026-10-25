# Open ONE .docx in Word, export the whole of it to PDF with heading bookmarks, write a success marker.
# Usage: powershell -File export_chunk.ps1 -Docx in.docx -Pdf out.pdf [-LimitSec 900]
#
# This is the only part of the big-book finalisation that uses Word, and it is deliberately given one
# document small enough to paginate inside memory. See finalize_big.py for why the book cannot be
# handed to Word whole.
#
# The export asks for CreateBookmarks=1 (heading bookmarks). That is not cosmetic: the PDF outline is
# how finalize_big.py learns which page each heading landed on, so it can build the table of contents
# without ever asking Word to paginate the whole book.
param([string]$Docx, [string]$Pdf, [int]$LimitSec = 1200, [switch]$Child, [string]$Marker)

if ($Child) {
  $ErrorActionPreference = "Stop"
  try {
    $w = New-Object -ComObject Word.Application
    $w.Visible = $false; $w.DisplayAlerts = 0
    $d = $w.Documents.Open($Docx, $false, $true)
    # (OutputFileName, Format=17 PDF, OpenAfterExport, OptimizeFor=0 print, Range=0 whole document,
    #  From, To, Item=0 content, IncludeDocProps, KeepIRM, CreateBookmarks=1 headings,
    #  DocStructureTags=false — tagged PDF roughly doubles both time and memory on these books)
    $d.ExportAsFixedFormat($Pdf, 17, $false, 0, 0, 0, 0, 0, $true, $true, 1, $false)
    Set-Content -Path $Marker -Value "ok"
    $d.Close(0); $w.Quit()
  } catch {
    Set-Content -Path $Marker -Value "error=$($_.Exception.Message)"
  }
  exit 0
}

Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep 2
Remove-Item $Pdf -Force -ErrorAction SilentlyContinue
$marker = [System.IO.Path]::GetTempFileName()
Remove-Item $marker -Force -ErrorAction SilentlyContinue
$p = Start-Process powershell -PassThru -WindowStyle Hidden -ArgumentList @(
  "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $PSCommandPath,
  "-Docx", $Docx, "-Pdf", $Pdf, "-Child", "-Marker", $marker)

# A frozen COM call cannot be timed out from inside the call, so the work runs in a child and the
# parent watches the clock and Word's memory. Peak memory is reported because it is the number that
# decides whether the chunking is still safe: if a chunk approaches the commit limit, chunks are too big.
$sw = [Diagnostics.Stopwatch]::StartNew(); $peakMB = 0
while ($sw.Elapsed.TotalSeconds -lt $LimitSec) {
  if (Test-Path $marker) { break }
  if ($p.HasExited) { break }
  Start-Sleep 5
  $wd = Get-Process WINWORD -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($wd) { $m = [int]($wd.WorkingSet64 / 1MB); if ($m -gt $peakMB) { $peakMB = $m } }
}
$res = if (Test-Path $marker) { ((Get-Content $marker) -join ' ').Trim() } else { "TIMEOUT-OR-CRASH" }
Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Remove-Item $marker -Force -ErrorAction SilentlyContinue
"{0,-26} {1,5:n0}s  peak={2,5}MB  {3}" -f (Split-Path $Docx -Leaf), $sw.Elapsed.TotalSeconds, $peakMB, $res
if ($res -ne "ok") { exit 1 }
