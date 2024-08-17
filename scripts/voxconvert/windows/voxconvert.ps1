param (
    [string]$command,
    [string]$command_str
)

$EXIT_CODE_SUCCESS=0
$EXIT_CODE_ERROR_EXECUTING_VOXCONVERT=10
$EXIT_CODE_ERROR_UNSUPPORTED_ARCH=11 # Error code on mac when architecuture is other than arm64 or x86_64
$EXIT_CODE_ERROR_ROSETTA_NOT_INSTALLED=12 # Error code on mac arm64 architecture

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

$args = Get-FormattedArgs -commandStr $command_str
Write-Host "${command} ```n$args" 

Invoke-Expression $command_str
if ($LASTEXITCODE -eq 0) {
    exit $EXIT_CODE_SUCCESS
}
[Console]::Error.WriteLine("`nExecuted command:")
[Console]::Error.WriteLine("${command} ```n$args")
exit $EXIT_CODE_ERROR_EXECUTING_VOXCONVERT
