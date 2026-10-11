# Opens the built .docx in Microsoft Word (COM), updates TOC + page-number fields, saves, exports the PDF.
# Usage:  powershell -File finalize_word.ps1 -Docx "E:\path\Book_Vyakhya.docx" [-ChunkPages 200] [-SkipUpdate]
# Why Word: python-docx / the Node docx library only *insert* a TOC field; only Word can compute the real
# page numbers. LibreOffice does not update the field reliably.
# Slow for big books: ~500 pages of Devanagari + tables can take 30-60 min; 1500+ pages 1-2 h. Run it
# detached (scheduled task or background) and wait.
# Robustness (learned on a 1500-page book):
#  * a hidden Word instance sometimes blocks forever inside a COM call (about 1 launch in 4) — every step
#    therefore runs in a child process under a watchdog: if WINWORD's CPU time stops growing for
#    -IdleMinutes, the step is killed and retried;
#  * Word's single-shot PDF export crashes on 1000+ pages — the export is done in page-range chunks and
#    merged with PyMuPDF; the docx is saved right after the TOC update, so -SkipUpdate resumes after a crash.
param(
  [string]$Docx = $env:OUT,
  [int]$ChunkPages = 200,
  [switch]$SkipUpdate,
  [int]$IdleMinutes = 8,
  [string]$Step = "all",   # internal: update | count | export
  [int]$From = 0, [int]$To = 0, [string]$Out = ""
)
if (-not $Docx) { Write-Error "Pass -Docx <path> (or set OUT env var)"; exit 1 }
$ErrorActionPreference = "Stop"
$pdf = [System.IO.Path]::ChangeExtension($Docx, ".pdf")
$dir = Split-Path $Docx
$stem = [System.IO.Path]::GetFileNameWithoutExtension($Docx)
$chunkDir = Join-Path $dir ($stem + "_pdfchunks")
$pagesFile = Join-Path $dir ($stem + ".pages")
$stamp = { "[" + (Get-Date -Format HH:mm:ss) + "]" }

function Open-Word {
  $w = New-Object -ComObject Word.Application
  $w.Visible = $false; $w.DisplayAlerts = 0
  return $w
}

# ---------------- child steps ----------------
if ($Step -eq "update") {
  $w = Open-Word
  $d = $w.Documents.Open($Docx)
  $d.Fields.Update() | Out-Null
  foreach ($t in $d.TablesOfContents) { $t.Update() }
  $d.Repaginate()
  foreach ($t in $d.TablesOfContents) { $t.UpdatePageNumbers() }
  $d.Save()
  $p = $d.ComputeStatistics(2)
  Set-Content -Path $pagesFile -Value $p          # success marker (written before the slow Close/Quit)
  "pages: $p"
  $d.Close(0); $w.Quit()
  exit 0
}
if ($Step -eq "count") {
  $w = Open-Word
  $d = $w.Documents.Open($Docx, $false, $true); $d.Repaginate(); $p = $d.ComputeStatistics(2)
  Set-Content -Path $pagesFile -Value $p
  "pages: $p"
  $d.Close(0); $w.Quit()
  exit 0
}
if ($Step -eq "export") {
  $w = Open-Word
  $d = $w.Documents.Open($Docx, $false, $true)
  # ExportAsFixedFormat(OutputFileName, ExportFormat=17 PDF, OpenAfterExport, OptimizeFor=0 print,
  #   Range=3 wdExportFromTo, From, To, Item=0 content, IncludeDocProps, KeepIRM,
  #   CreateBookmarks=1 headings, DocStructureTags=false (tagged PDF overloads Word on big books))
  $d.ExportAsFixedFormat($Out, 17, $false, 0, 3, $From, $To, 0, $true, $true, 1, $false)
  Set-Content -Path "$Out.done" -Value "ok"          # success marker
  $d.Close(0); $w.Quit()
  exit 0
}

# ---------------- orchestrator ----------------
function Clear-WordState {
  Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
  Remove-Item "HKCU:\Software\Microsoft\Office\16.0\Word\Resiliency" -Recurse -Force -ErrorAction SilentlyContinue
  Get-ChildItem $dir -Force -Filter "~`$*" -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
  Start-Sleep 3
}
# $marker = file the child writes when its real work is done (Word's Close/Quit afterwards can take
# 10+ minutes with no CPU, which must not be mistaken for a hang).
function Invoke-Step([string]$name, [string[]]$extra, [string]$marker, [int]$tries = 4) {
  for ($try = 1; $try -le $tries; $try++) {
    Clear-WordState
    Remove-Item $marker -Force -ErrorAction SilentlyContinue
    $args = @("-NoProfile", "-ExecutionPolicy", "Bypass", "-File", $PSCommandPath, "-Docx", $Docx, "-Step", $name) + $extra
    $log = Join-Path $dir ($stem + ".step.log")
    $p = Start-Process powershell -ArgumentList $args -PassThru -WindowStyle Hidden -RedirectStandardOutput $log -RedirectStandardError "$log.err"
    $lastCpu = -1.0; $lastChange = Get-Date; $done = $false
    while (-not $p.HasExited) {
      Start-Sleep 20
      if (Test-Path $marker) {
        # work finished; give Word a few minutes to close cleanly, then move on regardless
        $done = $true
        if (-not $p.WaitForExit(300000)) { "$(& $stamp) $name : done, Word slow to quit - killing it"; Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue }
        break
      }
      $w = Get-Process WINWORD -ErrorAction SilentlyContinue | Sort-Object StartTime -Descending | Select-Object -First 1
      $cpu = if ($w) { [double]$w.CPU } else { -1.0 }
      if ($cpu -ne $lastCpu) { $lastCpu = $cpu; $lastChange = Get-Date }
      if (((Get-Date) - $lastChange).TotalMinutes -ge $IdleMinutes) {
        "$(& $stamp) $name $extra : Word idle for $IdleMinutes min (cpu=$cpu) - killing, retry $try"
        Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
        break
      }
    }
    if ($done -or (Test-Path $marker)) { Get-Content $log -ErrorAction SilentlyContinue | ForEach-Object { "$(& $stamp) $name : $_" }; return $true }
    "$(& $stamp) $name $extra : failed (try $try)"; Get-Content "$log.err" -ErrorAction SilentlyContinue | Select-Object -First 3
  }
  return $false
}

"$(& $stamp) start: $Docx"
if (-not $SkipUpdate) {
  if (-not (Invoke-Step "update" @() $pagesFile)) { Write-Error "TOC update failed"; exit 2 }
} elseif (-not (Test-Path $pagesFile)) {
  if (-not (Invoke-Step "count" @() $pagesFile)) { Write-Error "page count failed"; exit 2 }
}
$pages = [int](Get-Content $pagesFile)
"$(& $stamp) pages: $pages"

if (Test-Path $chunkDir) { Remove-Item $chunkDir -Recurse -Force }
New-Item -ItemType Directory $chunkDir | Out-Null
$from = 1; $n = 0
while ($from -le $pages) {
  $to = [Math]::Min($from + $ChunkPages - 1, $pages); $n++
  $out = Join-Path $chunkDir ("{0:d3}.pdf" -f $n)
  if (-not (Invoke-Step "export" @("-From", $from, "-To", $to, "-Out", $out) "$out.done")) { Write-Error "chunk $n failed"; exit 3 }
  "$(& $stamp) chunk $n : pages $from-$to ok ($([int]((Get-Item $out).Length/1KB)) KB)"
  $from = $to + 1
}
Clear-WordState

$py = @"
import sys, glob, fitz
out = fitz.open()
for f in sorted(glob.glob(sys.argv[1] + '/[0-9][0-9][0-9].pdf')): out.insert_pdf(fitz.open(f))
out.save(sys.argv[2], garbage=3, deflate=True)
print('merged pages:', out.page_count)
"@
$tmp = Join-Path $chunkDir "merge.py"; Set-Content -Path $tmp -Value $py -Encoding utf8
python $tmp $chunkDir $pdf
if ($LASTEXITCODE -eq 0) {
  Remove-Item $chunkDir -Recurse -Force
  Remove-Item (Join-Path $dir ($stem + ".step.log")), (Join-Path $dir ($stem + ".step.log.err")), $pagesFile -ErrorAction SilentlyContinue
}
"$(& $stamp) pages: $pages"
"$(& $stamp) pdf: $pdf"
