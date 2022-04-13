# Marinelink(blockchain platform)

The code was written to create a reliable bill of lading platform by placing the bill of lading on the blockchain.
if you want to know our service, please read below pdf file
https://drive.google.com/file/d/1SbVk5AhKQOhFacigZ9U7W1alNZ_A-Tjx/view?usp=sharing

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
2. Make contract for uploading some information about BL
2. User-initiated contract list lookup
3. Download the pdf file for the contract you proceeded
4. Return sha256 code of pdf generated from contract
5. User selected contract basic information inquiry
![login](https://user-images.githubusercontent.com/35265981/163111079-216e02c3-e8ee-451f-b9c3-9202a2164b13.png)
![contract 확인](https://user-images.githubusercontent.com/35265981/163111047-d0e6b152-838b-4878-825a-1725f75eef37.png)
![선하증권페이지](https://user-images.githubusercontent.com/35265981/163111085-a554aaaa-26a9-43d0-9e4c-a65875f9c2af.png)
![makecontract](https://user-images.githubusercontent.com/35265981/163111084-b9832943-0652-46c9-8ac4-2e0c84fc8436.png)


## Built With

* [React](https://github.com/facebook/react) - The web framework used
* [FastAPI](https://github.com/tiangolo/fastapi) - The web framework used
* [React Soft Dashboard](https://github.com/app-generator/react-soft-ui-dashboard) -Template
## Contributing

