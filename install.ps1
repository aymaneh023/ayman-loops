# Links every skill in skills/ into Claude Code (Windows junctions). Safe to run again.
$root = "$HOME\.claude\skills"
New-Item -ItemType Directory -Force $root | Out-Null
foreach ($skill in Get-ChildItem "$PSScriptRoot\skills" -Directory) {
    $link = Join-Path $root $skill.Name
    if (Test-Path $link) {
        # Leave a real folder alone; it is not ours to replace.
        if ((Get-Item $link).LinkType -ne 'Junction') { Write-Warning "skip $link (exists, not a link)" }
        continue
    }
    New-Item -ItemType Junction -Path $link -Target $skill.FullName | Out-Null
    Write-Output "linked $link"
}
