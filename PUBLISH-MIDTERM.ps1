$ErrorActionPreference = 'Stop'
$expected = 'b2fce97027dc61bd73a4ce6fab71488ffbe3f738'
$repoUrl = 'https://github.com/s2005on/vnu-food-hola.git'
$branch = 'fix/midterm-completion-' + (Get-Date -Format 'yyyyMMdd-HHmmss')
$dest = Join-Path (Split-Path $PSScriptRoot -Parent) ('vju-midterm-git-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
function GitChecked {
    & git @args
    if ($LASTEXITCODE -ne 0) { throw 'Git failed. Stopped; keep this window output for diagnosis.' }
}
Get-Command git -ErrorAction Stop | Out-Null
GitChecked clone --branch main $repoUrl $dest
Push-Location $dest
try {
    $head = (& git rev-parse HEAD).Trim()
    if ($head -ne $expected) { throw 'main changed since this package. Stopped before copying; review the new main first.' }
    $name = & git config user.name
    $email = & git config user.email
    if (-not $name -or -not $email) {
        $name = Read-Host 'Git author name'
        $email = Read-Host 'Git author email'
        if (-not $name -or -not $email) { throw 'Author identity is required.' }
        GitChecked config user.name $name
        GitChecked config user.email $email
    }
    GitChecked switch -c $branch
    $files = @(
        'README.md', 'START-HERE.md', 'VERIFICATION.md', 'MIDTERM-UPDATE.md', 'PUBLISH-MIDTERM.ps1',
        '.github/workflows/backend-ci.yml', 'deploy/README.md', 'deploy/install-v4.sh', 'deploy/verify-public.sh',
        'docs/03-system-design.md', 'docs/MIDTERM.md', 'docs/PR-REVIEW.md',
        'docs/evidence/midterm-backend.txt', 'docs/evidence/midterm-javascript.txt'
    )
    foreach ($file in $files) {
        $target = Join-Path $dest $file
        New-Item -ItemType Directory -Force -Path (Split-Path $target -Parent) | Out-Null
        Copy-Item -LiteralPath (Join-Path $PSScriptRoot $file) -Destination $target -Force
    }
    GitChecked diff --check
    GitChecked add -- @files
    GitChecked commit -m 'fix: complete midterm documentation and deployment checks'
    GitChecked push -u origin $branch
    Write-Host "Create PR: https://github.com/s2005on/vnu-food-hola/compare/main...$branch"
} finally { Pop-Location }
