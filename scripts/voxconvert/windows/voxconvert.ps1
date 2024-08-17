param (
    [string]$command,
    [string]$command_str
)

#Uncomment to test for error
#$command_str = '& "C:\Users\harry\AppData\Roaming\Blender Foundation\Blender\4.0\scripts\addons\voxility_pro\voxconvert-executable\0.0.29\windows\vengi-voxconvert.exe" --script fillhollow -set metric_flavor json -set voxformat_scale 1.0 -set voxformat_voxelizemode 0 -set voxformat_ambientocclusion 0 -set voxformat_withcolor 0 -set voxformat_mergequads 0 -set palette built-in:nippon -set voxformat_fillhollow 1 --input "C:\Users\harry\AppData\Local\Temp\vxv1.0.14-bv4.0.1-tmpCGuGD\exppwopo\temp.qb" --output "C:\Users\harry\OneDrive\Documents\bbb.vox" --force'

function Get-FormattedArgs {
    param (
        [string]$commandStr
    )
    $voxIndex = $commandStr.IndexOf("vox")
    if ($voxIndex -eq -1) {
        return "No 'vox' found in command string."
    }
    $commandSubStr = $commandStr.Substring($voxIndex)
    $splitArgs = [regex]::Split($commandSubStr, ' (?=-|--)', [System.Text.RegularExpressions.RegexOptions]::None)
    return ($splitArgs[1..($splitArgs.Length - 1)] -join " ```n")
}

#Write-Host "$PSCommandPath" -ForegroundColor Blue
$args = Get-FormattedArgs -commandStr $command_str
Write-Host "${command} ```n$args" 

Invoke-Expression $command_str
if ($LASTEXITCODE -eq 0) {
    exit 0
}
[Console]::Error.WriteLine("`nExecuted command:")
[Console]::Error.WriteLine("${command} ```n$args")
exit 10
