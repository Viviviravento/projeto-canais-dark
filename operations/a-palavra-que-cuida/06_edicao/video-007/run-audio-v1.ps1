$python = "C:\Users\Vivia\OneDrive\Desktop\Projeto Canais Dark\tools\OpenMontage\.venv\Scripts\python.exe"
$script = "C:\Users\Vivia\OneDrive\Desktop\Projeto Canais Dark\operations\a-palavra-que-cuida\scripts\run-video-007-audio-v1.py"
$log = "C:\Users\Vivia\OneDrive\Desktop\Projeto Canais Dark\operations\a-palavra-que-cuida\06_edicao\video-007\audio-v1.log"
Set-Content -LiteralPath $log -Value "AUDIO_STARTED=$(Get-Date -Format o)"
& $python $script --commit-paid-call --approved-maximum-credits 9000 --user-statement "continua" *>> $log
$exit = $LASTEXITCODE
Add-Content -LiteralPath $log -Value "AUDIO_EXIT_CODE=$exit"
