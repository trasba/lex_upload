# lex_upload

A Python project to upload files (vouchers/Beleg) to the lexoffice api.
It monitors a given folder, if a new file is detected the file is
* verified to be a valid pdf
* uploaded to lexoffice
* moved from the upload folder to a folder according to what happend
  * accepted -> 202 folder
  * upload failure -> 4xx folder (e.g. on authorization failure)
  * not a valid pdf -> corrupted folder

## Getting Started
---
 * install package
 ```
 pip3 install https://github.com/trasba/lex_upload/raw/master/dist/lex_upload-0.1.0-py3-none-any.whl
 ```
 * get your api key here https://app.lexoffice.de/addons/public-api
 * create config.json under your home directory e.g. /home/user/.trasba/lex_uplaod/config.json e.g.
 ```
 {
    "api_key":"created_api_key",
    "202":"/yourpath/upload/202/",
    "4xx":"/yourpath/upload/4xx/",
    "upload":"/yourpath/upload/",
    "corrupt":"/yourpath/upload/corrupt/"
}
 ```
* run lex_upload
```
python -m lex_upload.main
```
* drop files to the upload folder

## FAQ
---
Where is the log?
> The log is written to file `log` in the `/home/<user>/.trasba/lex_upload` folder

## License
---
MIT