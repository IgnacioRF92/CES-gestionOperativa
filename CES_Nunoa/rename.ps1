$baseDir = "c:\Users\CES\Desktop\gestion CES\Codigo_CES_Nunoa_v34\CES_Nunoa\dist"
$htmlFiles = Get-ChildItem -Path $baseDir -Recurse -Filter *.html

$fileMap = @{}
foreach ($file in $htmlFiles) {
    if ($file.Name -eq "index.html" -and $file.DirectoryName -ne $baseDir) {
        $newName = $file.Directory.Name + ".html"
        $newFullName = Join-Path $file.DirectoryName $newName
        $fileMap[$file.FullName] = $newFullName
        Rename-Item -Path $file.FullName -NewName $newName
        Write-Host "Renamed $($file.FullName) to $newName"
    }
}

$htmlFiles = Get-ChildItem -Path $baseDir -Recurse -Filter *.html

foreach ($file in $htmlFiles) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    $evaluator = [System.Text.RegularExpressions.MatchEvaluator] {
        param($match)
        $quote = $match.Groups[1].Value
        $url = $match.Groups[2].Value
        
        # Skip absolute URLs, data URIs, anchors, and ones that already have an extension
        if ($url -match "^(http|mailto|tel|data):" -or $url.StartsWith("#") -or $url -match "\.[a-zA-Z0-9]+($|#)") {
            return $match.Value
        }

        # Split path and hash
        $hashIdx = $url.IndexOf("#")
        $path = $url
        $hash = ""
        if ($hashIdx -ge 0) {
            $path = $url.Substring(0, $hashIdx)
            $hash = $url.Substring($hashIdx)
        }

        if ([string]::IsNullOrEmpty($path)) {
            return $match.Value
        }

        # Resolve the directory
        try {
            # Combine the current file's directory with the path
            $targetPath = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine($file.DirectoryName, $path))
            $targetDirInfo = Get-Item $targetPath -ErrorAction SilentlyContinue
            
            if ($targetDirInfo -is [System.IO.DirectoryInfo]) {
                if ($targetPath.TrimEnd('\','/') -eq $baseDir.TrimEnd('\','/')) {
                    $path = $path + "index.html"
                } else {
                    $path = $path + $targetDirInfo.Name + ".html"
                }
            }
        } catch {
            Write-Host "Error resolving path $path"
        }
        
        return "href=$quote$path$hash$quote"
    }
    
    $newContent = [System.Text.RegularExpressions.Regex]::Replace($content, 'href=(["''])(.*?)\1', $evaluator)
    
    if ($content -ne $newContent) {
        Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
        Write-Host "Updated links in $($file.FullName)"
    }
}
