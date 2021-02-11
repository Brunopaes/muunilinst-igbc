# muunilinst-igbc

![GitHub language count](https://img.shields.io/github/languages/count/Brunopaes/octo-template.svg)
![GitHub top language](https://img.shields.io/github/languages/top/Brunopaes/octo-template.svg)
![GitHub repo size](https://img.shields.io/github/repo-size/Brunopaes/octo-template.svg)
![GitHub](https://img.shields.io/github/license/Brunopaes/octo-template.svg)

<small>_Optimized for python 3.6+_</small>

The Intergalactic Banking Clan (IGBC), also known simply as the Galactic 
Banking Clan or as the Banking Clan, was one of the most influential commerce 
guilds during the waning days of the Galactic Republic and the most
important organization in the Outer Rim.

----------------------

## Dependencies

For installing the requirements, in your ___venv___ or ___anaconda env___, 
just run the following command:

```shell script
pip install -r requirements.txt
```
----------------

## Project's Structure

```bash 
.
└── muunilinst-igbc
    ├── docs
    │   └── CREDITS
    ├── src
    │   ├── __init__.py
    │   └── settings.json
    ├── tests
    │   └── unittests
    │       └── __init__.py
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    └── requirements.txt
```

#### Directory description

- __data:__ The data dir. Group of non-script support files.
- __docs:__ The documentation dir.
- __src:__ The scripts & source code dir.
- __tests:__ The unittests dir.

----------------

## Usage Notes

Section aimed on clarifying some running issues.

### Running

For running it, at the `~/src` directory just run:

```shell script
python btc-inserter.py
``` 

or, if importing it as a module, just run:
````python
from btc_inserter import BTCoin

if __name__ == '__main__':
    BTCoin().__call__()
````

### JSON structure

````json
{
  "type": "sjdnjsnda",
  "project_id": "blabla-3219392",
  "private_key_id": "sdad48asd8asdas4das54dasd4",
  "private_key": "-----BEGIN PRIVATE KEY----------END PRIVATE KEY-----\n",
  "client_email": "sdasdsaf@sadsd.iam.gserviceaccount.com",
  "client_id": "6265262562323265523232",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509"
}
````

_obs: in order to run this application you must have a json file at 
`~/src/gcp-credentials.json`. This json must follow the structure above._

### database table schema

In order to start storing the btc historical prices, you must have a table
similar to the following table.

| ROW | OPERATION | PRICE   | DATETIME             |
|-----|-----------|---------|----------------------|
| 1   | buy       | 250000  | 2021-02-11 04:00:00  |
| 2   | sell      | 255000  | 2021-02-11 04:00:00  |
| 3   | buy       | 250000  | 2021-02-11 05:00:00  |
| 4   | sell      | 249000  | 2021-02-11 05:00:00  |
| 5   | buy       | 248000  | 2021-02-11 06:00:00  |
| 6   | sell      | 250000  | 2021-02-11 07:00:00  |

---------------
