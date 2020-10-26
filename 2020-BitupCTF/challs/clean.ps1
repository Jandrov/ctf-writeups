$flag = "MW1/IXwfKTsNE38+eBM5fDU3fH48OTglLg=="

function fun1 {
    param (
      [Parameter(Position = 0 ,          Mandatory = $true)] [string] $var,
      [Parameter(Position = 1 ,          Mandatory = $true)] [byte] $var_byte
    )

    $v2 = [System.Convert]::FromBase64String( $var )

    for ($QNV = 0; $QNV -lt $v2.length; $QNV++ ) {
        $v2[$QNV] = $v2[$QNV] -bxor $var_byte
    }

    return  [System.Text.Encoding]::ASCII.GetString($v2 )                                
}

Function reverse {
    param
    (
        [parameter(Position = 0, Mandatory = $true)] [string[]] $var
    )

    Process
    {
        ForEach ($char in $var) {
            ([regex]::Matches($char,'.','RightToLeft') | ForEach {$_.value}) -join ''
        }
    }
}

Function tobase64 {
    param
    (
        [parameter(Position = 0,  Mandatory = $true)] [string[]] $var      
    )

    $v1 = [System.Text.Encoding]::ASCII.GetBytes($var)
    $v2 =[Convert]::ToBase64String($v1) 
                                                                                             
    return $v2                   
  }

Function fun4 {
    param
    (
        [parameter(Position = 0 ,  Mandatory = $true)] [string[]] $mvlkmlslkq
    )
    $var = [System.Text.Encoding]::ASCII.GetString([System.Convert]::FromBase64String($mvlkmlslkq))
    return $var
}

$input = Read-Host -Prompt 'Input your flag: '
$var1 = 'RightToLeft'
$var1 = tobase64 $input                      
$var2 = fun1 $var1 0x4c
$var3 = reverse "blVbVEhoU3BZWkg="
$var4 = reverse $var2
$var3 = tobase64 $var4

if ( $var3 -eq $flag ) {
  Write-Output "[*] The flag: '$input' is correct :)"
} else {
  Write-Output "[!] The flag: '$input' is not correct :("
}