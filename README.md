# winrw - Proof of concept of a ransomware

## What is winrw?
winrw (***Win***dows ***r***ansom***w***are, I know it's an original name lol) is a part of an assignment for a bootcamp in cybersecurity.

## Disclaimer
This project is meant for educational purposes, cybersecurity researches and similar stuff. This repository doesn't include any downloadable binaries and it's not meant to be used as an actual piece of malware. Don't do anything illegal with my stuff!

## Inner workings
* It searches for *.txt, *.pdf, *.doc, *.docx, *.rtf in the directory `C:\Users\<username>\Desktop\keepcoding`.
* It uploads the files to a simulated botnet (using a virtual machine running Ubuntu).
* It encrypts the files with hybrid encryption.
* It deletes the original files.
* It leaves a public key and an encrypted symmetrical key.

## Considerations
The whole code and comments are in Spanish.

## Room for improvement
* Code obfuscation.
* Check for existing files so it doesn't overwrite them.
* Check if the files are already being used by another process.
* Better permission managements so it doesn't have to delete the old keys.
* Creating folders to sort files by victim.
* ~~Use of magic numbers instead of file extensions.~~ Fixed in version 1.1.
* Add persistence.
