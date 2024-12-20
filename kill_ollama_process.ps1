# Define the local port to target ollama service if running
$LocalPort = 11434

$Process = Get-NetTCPConnection -LocalPort $LocalPort | Select-Object -ExpandProperty OwningProcess

if ($Process) {
    # Display details and kill the process
    $ProcessDetails = Get-Process -Id $Process
    Write-Output "Process details:"
    Write-Output $ProcessDetails

    Stop-Process -Id $Process -Force
    Write-Output "Process with ID $Process has been terminated."
} else {
    Write-Output "No process found using port $LocalPort."
}