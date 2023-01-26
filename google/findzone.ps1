$c = (Select-String -Path "set_defaults.ps1" -Pattern "zone")
$w = ($c -split "=")
echo $w[2]
