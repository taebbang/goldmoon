# Marinelink(blockchain platform)

The code was written to create a reliable bill of lading platform by placing the bill of lading on the blockchain.

## Getting Started

python == 3.6.9
ubuntu 18.04
npm == 6.14.16

### Prerequisites
this code consist of fastAPI and React. so you need to install some package

What things you need to install the package and how to install them

```
git clone https://github.com/taebbang/goldmoon.git
cd marinelink
pip install -r requirement.txt
```

### Installing
if you want to run fastapi server , you have to change some code

```
cd util
```
you can find the constant.py and modify below line

```
G_PROJECT_BASE_DIR = r'YOUR PROJECT DIRECTORY'
```
and run server

```
python3 main.py
```

and if you want to run web server you have to change some port in 

```
cd web-src/src/config
vi constant.js
```
```
npm start run
```

## explanation

This web is the initial version of the platform where bills of lading can be raised and checked. 
Features implemented include:
1. Sign up for membership and log in
2. User-initiated contract list inquiry
3. Download the pdf file for the contract you proceeded
4. Return sha256 code of pdf generated from contract
5. User selected contract basic information inquiry


## Built With

* [React](https://github.com/facebook/react) - The web framework used
* [FastAPI](https://github.com/tiangolo/fastapi) - The web framework used

## Contributing

