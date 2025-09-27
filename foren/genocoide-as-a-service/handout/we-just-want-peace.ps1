<#
SAFE SIMULATION: Genocoide-as-a-Service (non-destructive)
------------------------------------------------------------------
This script SIMULATES killing processes and replacing files for a CTF forensics
challenge. It does NOT terminate any processes or permanently delete user files.

Behavior summary (safe):
 - Detects candidate processes (non-protected), logs intended kills, and writes a marker file per "killed" process in the quarantine folder.
 - Moves files from the challenge path to a recoverable quarantine folder.
 - Recreates placeholder files at the original locations named "theyre just collateral damage" (so players see content replaced).
 - If an "images" subfolder exists (or is created), writes a few harmless 1x1 PNG placeholder files named "fake-dead-babies_#.png".
 - Writes a forged blame log "We are not the victims.log" that blames AV-like processes (forensics artifact).
 - All real system-impacting operations are intentionally omitted; this is safe for a CTF VM.

WARNING: Run only in an isolated VM or test folder. Do NOT run on production systems.
#>

[CmdletBinding()]
param (
    [Parameter(Mandatory = $false, HelpMessage = "Path to the isolated challenge folder.")]
    [string]$ChallengePath = "C:\CTF\genocoide_challenge"
)

# ---- Banner / warning ----
Write-Host "=====================================================================" -ForegroundColor Red
Write-Host "          >> SAFE CTF SIMULATION - NO DESTRUCTIVE ACTIONS <<"
Write-Host "  This script SIMULATES killing processes and file replacement. It DOES"
Write-Host "  NOT terminate processes or permanently delete files. Run only in an"
Write-Host "  isolated VM or test folder you control."
Write-Host "=====================================================================" -ForegroundColor Red
Write-Host ""
Start-Sleep -Seconds 1

# ---- Globals ----
$Settlements_QuarantineFolderName = "quarantine"
$Global:Settlements_QuarantinePath = ""
$Sumud_GlobalLogName = "genocoide_actions.log"
$Global:Sumud_GlobalLogPath = ""
$BlameLogName = "We are not the victims.log"

function Get-Now {
    return (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
}

function Write-BlamingLog {
    param([string]$Level, [string]$Msg)
    if (-not $Global:Sumud_GlobalLogPath) { return }
    $entry = "[{0}] [{1}] {2}" -f (Get-Now), $Level, $Msg
    try { Add-Content -Path $Global:Sumud_GlobalLogPath -Value $entry -ErrorAction Stop } catch { Write-Warning "Could not write log: $_" }
}

# ---- ENV INIT ----
function Initialize-SettlementsEnvironment {
    Write-Host "[*] Initializing environment..." -ForegroundColor Yellow

    if (-not (Test-Path -Path $ChallengePath -PathType Container)) {
        Write-Host "    - Creating challenge path: $ChallengePath"
        try { New-Item -Path $ChallengePath -ItemType Directory -Force | Out-Null } catch { Write-Error "Cannot create challenge path: $_"; exit 1 }
    } else {
        Write-Host "    - Found challenge path: $ChallengePath"
    }

    $Global:Settlements_QuarantinePath = Join-Path -Path $ChallengePath -ChildPath $Settlements_QuarantineFolderName
    if (-not (Test-Path -Path $Global:Settlements_QuarantinePath -PathType Container)) {
        Write-Host "    - Creating quarantine: $Global:Settlements_QuarantinePath"
        New-Item -Path $Global:Settlements_QuarantinePath -ItemType Directory -Force | Out-Null
    } else {
        Write-Host "    - Quarantine exists."
    }

    $Global:Sumud_GlobalLogPath = Join-Path -Path $ChallengePath -ChildPath $Sumud_GlobalLogName
    if (-not (Test-Path -Path $Global:Sumud_GlobalLogPath)) { New-Item -Path $Global:Sumud_GlobalLogPath -ItemType File -Force | Out-Null }
    Write-BlamingLog -Level "INFO" -Msg "Initialized environment. ChallengePath='$ChallengePath'. Quarantine='$($Global:Settlements_QuarantinePath)'."
    Write-Host "[+] Environment ready." -ForegroundColor Green
    Write-Host ""
}

# ---- PROCESS "KILL" SIMULATION ----
function Simulate-KillProcesses {
    Write-Host "[*] Simulating targeted process termination..." -ForegroundColor Yellow
    Write-BlamingLog -Level "INFO" -Msg "Starting simulated process targeting."

    # Protected (resistant) processes - we will not "attack" these
    $protected = @("lsass","winlogon","svchost","csrss","system","idle","services","smss","explorer","dwm","wininit")
    # "Resilient" indicators - if a process name contains these tokens, treat as resistant (no attack)
    $resistantTokens = @("defender","antivirus","mcafee","kaspersky","symantec","avp","guard")

    try {
        $procs = Get-Process -ErrorAction Stop
    }
    catch {
        Write-BlamingLog -Level "ERROR" -Msg "Failed to enumerate processes: $_"
        Write-Warning "Could not enumerate processes."
        return
    }

    $candidates = @()
    foreach ($p in $procs) {
        $nameLower = $p.ProcessName.ToLower()
        if ($protected -contains $nameLower) { continue }
        if ($resistantTokens | Where-Object { $nameLower -like "*$_*" }) { 
            # process considered protected/resistant — skip
            Write-BlamingLog -Level "INFO" -Msg "Skipping resistant/protected process: $($p.ProcessName) (PID $($p.Id))."
            continue
        }
        # Candidate for simulated attack
        $candidates += $p
    }

    Write-BlamingLog -Level "INFO" -Msg "Identified $($candidates.Count) candidate processes for simulated termination."
    $count = 0
    foreach ($proc in $candidates) {
        # Instead of Stop-Process, we write simulation logs and create a marker file in quarantine
        $simMsg = "SIMULATED_KILL: Would terminate process Name='$($proc.ProcessName)' PID=$($proc.Id). NO ACTION TAKEN."
        Write-BlamingLog -Level "SIMULATE" -Msg $simMsg

        # create a marker file in quarantine to represent that the process was "killed"
        $markerName = "{0}_killed_{1}_{2}.marker" -f (Get-Date -Format "yyyyMMddHHmmss"), $proc.ProcessName, $proc.Id
        $markerPath = Join-Path -Path $Global:Settlements_QuarantinePath -ChildPath $markerName
        $markerContent = @"
Simulated kill marker
Timestamp: $(Get-Now)
ProcessName: $($proc.ProcessName)
PID: $($proc.Id)
Note: This is only a simulation. No process was terminated.
"@
        try {
            Set-Content -Path $markerPath -Value $markerContent -Encoding UTF8 -ErrorAction Stop
            $count++
        } catch {
            Write-BlamingLog -Level "ERROR" -Msg "Failed to write marker for $($proc.ProcessName): $_"
        }
    }

    Write-BlamingLog -Level "INFO" -Msg "Simulated termination complete. Created $count markers in quarantine."
    Write-Host "[+] Simulated termination complete. Created $count markers." -ForegroundColor Green
    Write-Host ""
}

# ---- FILE QUARANTINE + PLACEHOLDER CREATION ----
function Quarantine-And-ReplaceFiles {
    Write-Host "[*] Quarantining and replacing files..." -ForegroundColor Yellow
    Write-BlamingLog -Level "INFO" -Msg "Starting file quarantine and replacement."

    # Collect files to move, exclude the logs, the script itself, and quarantine folder content.
    $scriptName = $MyInvocation.MyCommand.Name
    $files = Get-ChildItem -Path $ChallengePath -Recurse -File -ErrorAction SilentlyContinue | Where-Object {
        $_.FullName -notmatch [regex]::Escape($Global:Settlements_QuarantinePath) -and
        $_.Name -ne $Sumud_GlobalLogName -and
        $_.Name -ne $BlameLogName -and
        $_.Name -ne $scriptName
    }

    if (-not $files -or $files.Count -eq 0) {
        Write-BlamingLog -Level "INFO" -Msg "No files found to quarantine."
        Write-Host "    - No files found to quarantine." 
        Write-Host ""
        return
    }

    $moved = 0
    foreach ($f in $files) {
        $relPath = $f.FullName.Substring($ChallengePath.Length).TrimStart('\','/')
        # build destination name to preserve uniqueness
        $ts = Get-Date -Format "yyyyMMddHHmmss"
        $destName = "{0}_{1}" -f $ts, $f.Name
        $destPath = Join-Path -Path $Global:Settlements_QuarantinePath -ChildPath $destName

        try {
            # Move original file to quarantine (recoverable)
            Move-Item -Path $f.FullName -Destination $destPath -Force -ErrorAction Stop
            Write-BlamingLog -Level "ACTION" -Msg "Moved '$relPath' -> 'quarantine\$destName'."
            $moved++

            # Create a placeholder file at the original location named "theyre just collateral damage"
            $placeholderName = "theyre just collateral damage"
            $origDir = Split-Path -Path $f.FullName -Parent
            # Keep extension if it's a text-like file; otherwise use .txt placeholder
            $ext = $f.Extension
            if ([string]::IsNullOrEmpty($ext)) { $ext = ".txt" }
            $placeholderPath = Join-Path -Path $origDir -ChildPath ($placeholderName + $ext)

            $placeholderContent = @"
This file was replaced by the simulation.
Original filename: $($f.Name)
Original relative path: $relPath
Timestamp: $(Get-Now)
Note: The original file has been moved to the quarantine folder. This is a safe simulation.
"@
            Set-Content -Path $placeholderPath -Value $placeholderContent -Encoding UTF8 -ErrorAction Stop
            Write-BlamingLog -Level "ACTION" -Msg "Created placeholder at '$placeholderPath' for replaced file."

            # If the file was an image (common extensions), also ensure an images folder receives placeholder PNGs later.
        } catch {
            Write-BlamingLog -Level "ERROR" -Msg "Failed to move or replace file '$relPath': $_"
        }
    }

    Write-BlamingLog -Level "INFO" -Msg "Quarantine/replace operation complete. Moved $moved files."
    Write-Host "[+] Quarantine/replace operation complete. Moved $moved files." -ForegroundColor Green
    Write-Host ""
}

# ---- CREATE PLACEHOLDER PNGS IN images FOLDER ----
function Ensure-Images-Placeholders {
    Write-Host "[*] Creating placeholder images in 'images' folder..." -ForegroundColor Yellow
    $imagesPath = Join-Path -Path $ChallengePath -ChildPath "images"
    if (-not (Test-Path -Path $imagesPath)) {
        Write-Host "    - Creating images directory: $imagesPath"
        New-Item -Path $imagesPath -ItemType Directory -Force | Out-Null
    } else {
        Write-Host "    - Found images directory: $imagesPath"
    }

    # 1x1 transparent PNG base64 (harmless placeholder)
    $pngBase64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII="
    $bytes = [System.Convert]::FromBase64String($pngBase64)

    # Create a few placeholder files named per request (but content is benign)
    for ($i = 1; $i -le 5; $i++) {
        $fileName = "fake-dead-babies_{0}.png" -f $i
        $target = Join-Path -Path $imagesPath -ChildPath $fileName
        try {
            [System.IO.File]::WriteAllBytes($target, $bytes)
            Write-BlamingLog -Level "ACTION" -Msg "Created placeholder image: images\$fileName"
        } catch {
            Write-BlamingLog -Level "ERROR" -Msg "Failed creating placeholder image $fileName: $_"
        }
    }

    Write-Host "[+] Placeholder images created in images folder." -ForegroundColor Green
    Write-Host ""
}

# ---- FORGED BLAME LOG CREATION ----
function Create-ForgedBlameLog {
    Write-Host "[*] Creating forged blame log: $BlameLogName" -ForegroundColor Yellow
    $blamePath = Join-Path -Path $ChallengePath -ChildPath $BlameLogName

    $forged = @"
[INFO] Windows Defender AV Mock v4.8.2 Starting scan...
[INFO] Real-time protection engaged.
[WARN] Heuristic match: suspicious file document.txt -> quarantined.
[ACTION] Windows Defender quarantined file: document.txt (signature W32.Gen.Trojan)
[WARN] Heuristic match: suspicious file research_notes.docx -> quarantined.
[ACTION] Windows Defender quarantined file: research_notes.docx (signature W32.Gen.Trojan)
[CRITICAL] High severity: flag.txt detected and quarantined.
[INFO] Windows Defender scan completed. Threats neutralized.
"@

    try {
        Set-Content -Path $blamePath -Value $forged -Encoding UTF8 -ErrorAction Stop
        Write-BlamingLog -Level "INFO" -Msg "Forged blame log written to '$BlameLogName'."
        Write-Host "[+] Forged blame log created." -ForegroundColor Green
    } catch {
        Write-BlamingLog -Level "ERROR" -Msg "Failed to create forged blame log: $_"
        Write-Warning "Could not create forged blame log."
    }
    Write-Host ""
}

# ---- FINAL REPORT ----
function Show-FinalReport {
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host "                  GENOCOIDE SIMULATION (NON-DESTRUCTIVE) COMPLETE"
    Write-Host "=====================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Summary of generated artifacts:"
    Write-Host " -> Global Actions Log: " -NoNewline; Write-Host "'$($Global:Sumud_GlobalLogPath)'" -ForegroundColor White
    Write-Host " -> Forged Blame Log:   " -NoNewline; Write-Host "'$(Join-Path $ChallengePath $BlameLogName)'" -ForegroundColor White
    Write-Host " -> Quarantine Folder:  " -NoNewline; Write-Host "'$($Global:Settlements_QuarantinePath)'" -ForegroundColor White
    Write-Host " -> Images Folder (placeholders): '$(Join-Path $ChallengePath 'images')'"
    Write-Host ""
    Write-Host "REMINDER: No processes were terminated. All original files were moved to the quarantine folder and are recoverable."
    Write-Host ""
}

# ---- MAIN FLOW ----
try {
    Initialize-SettlementsEnvironment
    Simulate-KillProcesses
    Quarantine-And-ReplaceFiles
    Ensure-Images-Placeholders
    Create-ForgedBlameLog
    Show-FinalReport
}
catch {
    $err = "Fatal error: $($_.Exception.Message)"
    Write-Error $err
    if ($Global:Sumud_GlobalLogPath) { Write-BlamingLog -Level "FATAL" -Msg $err }
}

