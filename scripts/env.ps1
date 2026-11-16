$repoRoot = Split-Path -Parent $PSScriptRoot
$toolsBin = Join-Path $repoRoot '.tools\bin'
$env:Path = "$toolsBin;$env:Path"
$env:PDK_ROOT = Join-Path $repoRoot 'pdk\ciel\sky130\versions\e7a6777d157a9d94c7ac757457b9e4309e9e9000'
$env:PDK = 'sky130A'
