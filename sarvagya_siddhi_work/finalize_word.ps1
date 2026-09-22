# Opens the generated docx in Word, updates TOC/page fields, saves, exports PDF.
$docx = if ($env:OUT) { $env:OUT } else { "E:\Projects\JinAagam\Laghu_Sarvagya_Siddhi_Vyakhya.docx" }
$pdf  = [System.IO.Path]::ChangeExtension($docx, ".pdf")
$w = New-Object -ComObject Word.Application
$w.Visible = $false; $w.DisplayAlerts = 0
$d = $w.Documents.Open($docx)
$d.Fields.Update() | Out-Null
foreach ($t in $d.TablesOfContents) { $t.Update() }
$d.Repaginate()
foreach ($t in $d.TablesOfContents) { $t.UpdatePageNumbers() }
$d.Save()
$d.ExportAsFixedFormat($pdf, 17)
"pages: " + $d.ComputeStatistics(2)
$d.Close(0); $w.Quit()
