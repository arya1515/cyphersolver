param(
    [Parameter(Mandatory = $true)]
    [string]$ImagePath
)

Add-Type -AssemblyName System.Runtime.WindowsRuntime

function Await-WinRT {
    param(
        [Parameter(Mandatory = $true)]
        $Operation,
        [Parameter(Mandatory = $true)]
        [Type]$ResultType
    )

    $method = [System.WindowsRuntimeSystemExtensions].GetMethods() |
        Where-Object {
            $_.Name -eq 'AsTask' -and
            $_.IsGenericMethod -and
            $_.GetParameters().Count -eq 1
        } |
        Select-Object -First 1
    $task = $method.MakeGenericMethod($ResultType).Invoke($null, @($Operation))
    $task.Wait()
    return $task.Result
}

$storageFileType = [Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime]
$randomAccessStreamType = [Windows.Storage.Streams.IRandomAccessStream, Windows.Storage.Streams, ContentType = WindowsRuntime]
$bitmapDecoderType = [Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime]
$softwareBitmapType = [Windows.Graphics.Imaging.SoftwareBitmap, Windows.Graphics.Imaging, ContentType = WindowsRuntime]
$ocrResultType = [Windows.Media.Ocr.OcrResult, Windows.Foundation, ContentType = WindowsRuntime]
$ocrEngineType = [Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime]

$resolved = (Resolve-Path -LiteralPath $ImagePath).Path
$file = Await-WinRT ($storageFileType::GetFileFromPathAsync($resolved)) $storageFileType
$stream = Await-WinRT ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read)) $randomAccessStreamType
$decoder = Await-WinRT ($bitmapDecoderType::CreateAsync($stream)) $bitmapDecoderType
$bitmap = Await-WinRT ($decoder.GetSoftwareBitmapAsync()) $softwareBitmapType
$engine = $ocrEngineType::TryCreateFromUserProfileLanguages()
$result = Await-WinRT ($engine.RecognizeAsync($bitmap)) $ocrResultType
$result.Text
