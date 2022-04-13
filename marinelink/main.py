from typing import List

from fastapi import FastAPI, HTTPException, Security, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.dbModel import User, Contract
import models.responseModel as Model
from util.security import generate_token, string_encoding, check_token, token_encrypt, token_decrypt, \
    generate_contract_id, decode_people_info, get_pdf_file_checksum
import util.constant as const
from util.string_util import get_date_string
from util.io_util import copy_json, load_json, save_contract_info_to_json, save_json
from util.pdf_util import factoryModule
import os
import uvicorn


app = FastAPI()
app.mount("/web", StaticFiles(directory="web"), name="web")
templates = Jinja2Templates(directory="web")

security = HTTPBearer()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', response_class=HTMLResponse)
def hello():
    return f'<h1>hello main</h1>'


@app.post('/api/user', response_model=Model.ReturnResponseModel)
def signup(a_user: Model.RegisterModel):
    if len(User.select(id=a_user.id)) > 0:
        return 'Account already exists'
    try:
        hashed_password = string_encoding(a_user.pwd)
        user_index = User.get_index()
        user = User(user_index, a_user.id, hashed_password, a_user.email, a_user.phone, a_user.name, "", 0, 0)
        user.insert()

        return {
            "success": True,
            "message": "Success Sign Up",
            "data": None
        }
    except:
        return {
            "success": False,
            "message": "Failed to signup user",
            "data": None
        }


@app.put('/api/logout', response_model=Model.ReturnResponseModel)
def logout(a_user_id: Model.LogoutModel):
    try:
        user = User.select(id=a_user_id)[0]
        user.token_key = "empty"
        user.update()
    finally:
        return {
            "success": True,
            "message": "Success Logout",
            "data": None
        }


@app.post('/api/login', response_model=Model.ReturnResponseModel)
def login(a_user: Model.LoginModel):

    user: List[User] = User.select(id=a_user.id)
    if len(user) == 0:
        return HTTPException(status_code=401, detail='Invalid username')
    user: User = user[0]

    if not string_encoding(a_user.pwd) == user.pwd:
        return HTTPException(status_code=401, detail='Invalid password')
    user.token_key = string_encoding(generate_token())
    user.update()
    token = token_encrypt(f'{user.id}{const.G_TOKEN_SEP_KEYWORD}{user.token_key}')
    return {
            "success": True,
            "message": "Success Login",
            "data": {'token': token}
    }


@app.get('/api/refresh_token', response_model=Model.ReturnResponseModel)
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    user = check_token(token)
    if user is None:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }
    user.token_key = string_encoding(generate_token())
    user.update()
    token = token_encrypt(f'{user.id}{const.G_TOKEN_SEP_KEYWORD}{user.token_key}')

    return {
            "success": True,
            "message": "Success Login",
            "data": {'token': token}
    }


@app.get('/api/user', response_model=Model.ReturnResponseModel)
def get_user_info(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    사용자 정보를 조회하는 API
    :param credentials:
    :return:
    """
    token = credentials.credentials
    user = check_token(token)
    if user is None:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }

    return {
            "success": True,
            "message": "",
            "data": {'name': user.name, 'phone': user.phone, 'email': user.email}
    }


@app.get('/api/contract', response_model=Model.ReturnResponseModel)
def get_contract_list(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    사용자가 진행한 계약 목록을 조회하는 API
    :param credentials:
    :return:
    """
    token = credentials.credentials
    user = check_token(token)
    if user is None:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }

    contract_list: List[Contract] = Contract.select(consignor_index=user.index)
    contract_info_list = [{
        'id': contract.contract_id,
        'type': contract.contract_type,
        'hash': contract.contract_auth,
        'consignor_info': {
            'name': contract.consignor_name,
            'phone': contract.consignor_phone
        },
        'consignee_info': {
            'name': contract.consignee_name,
            'phone': contract.consignee_phone
        },
        'create_date': contract.create_date,
        'contract_date': contract.contracted_date,
        'status': contract.status
    } for contract in contract_list]
    return {
        "success": True,
        "message": "",
        "data": {'contract': contract_info_list}
    }


@app.get('/api/contract/usable', response_model=Model.ReturnResponseModel)
def get_usable_contract_list(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    현재 사용자가 신규로 진행할 수 있는 계약의 종류를 반환하는 API
    :param credentials:
    :return:
    """
    token = credentials.credentials
    user = check_token(token)
    if user is None:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }

    return {
        "success": True,
        "message": "",
        "data": {'options': const.G_CONTRACT_TYPE_MAP}
    }


@app.get('/api/contract/pdf/{contract_id}')
def get_contract_pdf(contract_id: str):
    """
    진행된 계약에 대한 pdf 파일을 download받는 API
    :param contract_id:
    :param credentials:
    :return:
    """
    try:
        contract = Contract.select(contract_id=contract_id)[0]
        return FileResponse(contract.contract_pdf_file_path, filename='contract.pdf')
    except Exception:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }


@app.get('/api/contract/auth/{contract_id}', response_model=Model.ReturnResponseModel)
def get_contract_auth_key(contract_id: str):
    """
    계약에서 생성된 pdf의 sha256 code를 가져오는 API
    :param contract_id:
    :return:
    """
    try:
        contract = Contract.select(contract_id=contract_id)[0]
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": contract.contract_auth
        }
    except Exception:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }


@app.get('/api/contract/info/default/{contract_type}', response_model=Model.ReturnResponseModel)
def get_contract_default_info(contract_type:str, credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    사용자가 선택한 contract의 기본 정보들을 가져오는 API
    :param credentials:
    :return:
    """
    token = credentials.credentials
    user = check_token(token)
    if user is None:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }
    contract_index = Contract.get_index()
    contract_id = generate_contract_id()

    src_path = os.path.join(const.G_CONTRACT_FORM_DIR, contract_type,
                            const.G_CONTRACT_BASE_FORMAT_FILE_NAME)
    # tar_path = os.path.join(const.G_CONTRACT_SAVE_FOLDER_PATH, contract_type, f'{contract_id}.json')
    tar_path = os.path.join(
        const.G_CONTRACT_SAVE_FOLDER_PATH,
        contract_type,
        const.G_CONTRACT_JSON_FOLDER_NAME,
        contract_id + '.json'
    )
    # copy_json(src_path, tar_path)
    contract = Contract(contract_index, contract_id, const.G_CONTRACT_AUTH_EMPTY_KEY,
                        const.G_CONTRACT_TYPE_MAP[contract_type], user.index, user.name, user.phone,
                        const.G_CONTRACT_SIGN_EMPTY_KEY, '', '', const.G_CONTRACT_SIGN_EMPTY_KEY,
                        tar_path, const.G_CONTRACT_FILE_EMPTY_KEY, get_date_string(),
                        None, const.G_CONTRACT_STATUS_MAP['created'], 0)
    # contract.insert()
    contract_default_info = load_json(src_path)
    contract_default_info['bl_no'] = generate_token()
    # contract_default_info['consignor']['name'] = user.name
    # contract_default_info['consignor']['TEL'] = user.phone
    # save_json(tar_path, contract_default_info)
    return {
            "success": True,
            "message": "",
            "data": {
                "contract_id": contract_id,
                "contract_info": contract_default_info,
                "name": user.name,
                "phone": user.phone
            }
        }


@app.get('/api/contract/info/{contract_id}', response_model=Model.ReturnResponseModel)
def get_contract_info(contract_id:str, credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    작성 중이거나 저장된 contract의 값을 조회하는 API
    :param credentials:
    :return:
    """
    token = credentials.credentials
    user = check_token(token)
    if user is None:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }
    try:
        contract = Contract.select(contract_id=contract_id)[0]
        if contract.status != const.G_CONTRACT_STATUS_MAP['done']:
            contract_info = load_json(contract.contract_json_file_path)
            return {
                "success": True,
                "message": "",
                "data": {
                    "contract_id": contract_id,
                    "contract_info": contract_info
                }
            }
        else:
            return {
                "success": False,
                "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
                "data": None
            }
    except:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }


@app.post('/api/contract/info', response_model=Model.ReturnResponseModel)
def save_contract_info(contract_model:Model.ContractModel, credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    현재 작성중인 contract를 저장하는 API
    :param credentials:
    :return:
    """
    token = credentials.credentials
    user = check_token(token)

    if user is None:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }
    try:
        try:
            contract = Contract.select(contract_id=contract_model.id)[0]
        except IndexError:
            contract_index = Contract.get_index()
            tar_path = os.path.join(
                const.G_CONTRACT_SAVE_FOLDER_PATH,
                contract_model.type,
                const.G_CONTRACT_JSON_FOLDER_NAME,
                contract_model.id + '.json'
            )
            contract = Contract(contract_index, contract_model.id, const.G_CONTRACT_AUTH_EMPTY_KEY,
                                const.G_CONTRACT_TYPE_MAP[contract_model.type], user.index, user.name, user.phone,
                                const.G_CONTRACT_SIGN_EMPTY_KEY, '', '', const.G_CONTRACT_SIGN_EMPTY_KEY,
                                tar_path, const.G_CONTRACT_FILE_EMPTY_KEY, get_date_string(),
                                None, const.G_CONTRACT_STATUS_MAP['created'], 0)
            contract.insert()
        contract.consignor_sign = const.G_CONTRACT_SIGN_EMPTY_KEY
        contract.consignee_sign = const.G_CONTRACT_SIGN_EMPTY_KEY
        contract.status = const.G_CONTRACT_STATUS_MAP['saved']
        contract.update()
        save_json(contract.contract_json_file_path, contract_model.info)
        return {
            "success": True,
            "message": "Save Success",
            "data": None
        }
    except:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }


@app.post('/api/contract/info/done', response_model=Model.ReturnResponseModel)
def done_contract_info(contract_model:Model.ContractModel, credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    현재 작성중인 contract를 저장하는 API
    :param credentials:
    :return:
    """
    token = credentials.credentials
    user = check_token(token)

    if user is None:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }
    try:
        try:
            contract = Contract.select(contract_id=contract_model.id)[0]
        except IndexError:
            contract_index = Contract.get_index()
            tar_path = os.path.join(
                const.G_CONTRACT_SAVE_FOLDER_PATH,
                contract_model.type,
                const.G_CONTRACT_JSON_FOLDER_NAME,
                contract_model.id + '.json'
            )
            contract = Contract(contract_index, contract_model.id, const.G_CONTRACT_AUTH_EMPTY_KEY,
                                const.G_CONTRACT_TYPE_MAP[contract_model.type], user.index, user.name, user.phone,
                                const.G_CONTRACT_SIGN_EMPTY_KEY, '', '', const.G_CONTRACT_SIGN_EMPTY_KEY,
                                tar_path, const.G_CONTRACT_FILE_EMPTY_KEY, get_date_string(),
                                None, const.G_CONTRACT_STATUS_MAP['created'], 0)
            contract.insert()

        save_json(contract.contract_json_file_path, contract_model.info)
        pdf_generator = factoryModule(contract, contract_model.info)
        pdf_generator.generate()
        contract.contract_pdf_file_path = pdf_generator.get_pdf_file_path()
        contract.status = const.G_CONTRACT_STATUS_MAP['before_checked']
        contract.update()

        return {
            "success": True,
            "message": "Save Success",
            "data": None
        }
    except:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }


@app.get('/api/contract/sign/{contract_id}', response_model=Model.ReturnResponseModel)
def get_contract_sign_status(contract_id:str, credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    작성 중이거나 저장된 contract의 값을 조회하는 API
    :param credentials:
    :return:
    """
    token = credentials.credentials
    user = check_token(token)
    if user is None:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }
    try:
        contract = Contract.select(contract_id=contract_id)[0]

        if contract.consignor_sign == const.G_CONTRACT_SIGN_EMPTY_KEY:
            consignor_sign = False
        else:
            consignor_sign = True
        if contract.consignee_sign == const.G_CONTRACT_SIGN_EMPTY_KEY:
            consignee_sign = False
        else:
            consignee_sign = True

        return {
            "success": True,
            "message": "",
            "data": {
                "consignor": consignor_sign,
                "consignee": consignee_sign,
                "status": contract.status,
                "type": contract.contract_type
            }
        }
    except:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }


@app.get('/api/contract/consignor/{contract_id}',  response_class=HTMLResponse)
def get_contract_html_to_consignor(request: Request, contract_id:str):
    """
    consignee가 현재 계약에 대한 정보 및 계약을 진행할 수 있는 버튼이 담겨진 정보를 볼 수 있는 HTML을 요청하는 API
    HTML을 반환해야 함
    :param contract_id:
    :return:
    """
    return templates.TemplateResponse("template/consignor_sign.html", {"request": request, "contract_id": contract_id})


@app.get('/api/contract/consignor/{contract_id}/{consignor_key}', response_model=Model.ReturnResponseModel)
def get_sign_info_consignor(contract_id: str, consignor_key: str):
    try:
        contract = Contract.select(contract_id=contract_id)[0]
        name, phone = decode_people_info(consignor_key)
        if (contract.consignor_name == name) and (contract.consignor_phone.replace('-', '') == phone.replace('-', '')):
            return FileResponse(contract.contract_pdf_file_path, filename='contract.pdf')
    except:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }


@app.post('/api/contract/sign/{contract_id}', response_model=Model.ReturnResponseModel)
def sign_consignor(contract_id: str, sign_model: Model.ContractPersonSignModel):
    contract = Contract.select(contract_id=contract_id)[0]

    token = token_encrypt(
        f'{sign_model.name}{const.G_TOKEN_SEP_KEYWORD}{sign_model.phone}{const.G_TOKEN_SEP_KEYWORD}{get_date_string()}')
    contract.consignor_sign = token
    contract.status_update()
    contract.contracted_date = get_date_string()
    contract.update()

    return {
            "success": True,
            "message": "Consignor Sign Success",
            "data": None
        }


@app.get('/api/contract/consignee/{contract_id}')
def get_contract_html_to_consignee(request: Request, contract_id:str):
    return templates.TemplateResponse("template/consignee_sign.html", {"request": request, "contract_id": contract_id})


@app.get('/api/contract/consignee/{contract_id}/{consignee_key}', response_model=Model.ReturnResponseModel)
def get_sign_info_consignee(contract_id: str, consignee_key: str):
    try:
        contract = Contract.select(contract_id=contract_id)[0]
        name, phone = decode_people_info(consignee_key)
        if (contract.consignee_name == name) and (contract.consignee_phone.replace('-', '') == phone.replace('-', '')):
            return FileResponse(contract.contract_pdf_file_path, filename='contract.pdf')
    except:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }


@app.post('/api/contract/{contract_id}', response_model=Model.ReturnResponseModel)
def sign_consignee(contract_id: str, sign_model: Model.ContractPersonSignModel):
    contract = Contract.select(contract_id=contract_id)[0]

    token = token_encrypt(
        f'{sign_model.name}{const.G_TOKEN_SEP_KEYWORD}{sign_model.phone}{const.G_TOKEN_SEP_KEYWORD}{get_date_string()}')
    contract.consignee_sign = token
    contract.status_update()
    contract.update()

    return {
            "success": True,
            "message": "Consignor Sign Success",
            "data": None
        }


@app.post('/api/contract', response_model=Model.ReturnResponseModel)
def run_contract(contract_model:Model.RunContractModel, credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    consignor와 consignee가 모두 sign한 이후 실제 계약을 요청하는 API
    1. consignor와 consignee가 모두 sign했는지 확인
    2. 내부적으로 생성된 PDF 에대해서 sha256 check sum 코드 생성
    3. PDF 파일 전송 및 ID 및 다운로드 링킄 제공
    4. check sum 코드를 이더리움 메인넷에 contract id : key 가 되도록 하는 함수 등록

    PDF 생성 로직
    :param credentials:
    :return:
    """
    token = credentials.credentials
    user = check_token(token)
    if user is None:
        return {
                "success": False,
                "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
                "data": None
            }
    try:
        contract = Contract.select(contract_id=contract_model.contract_id)[0]
    except:
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }
    if (contract.consignor_sign == const.G_CONTRACT_SIGN_EMPTY_KEY) or (contract.consignee_sign == const.G_CONTRACT_SIGN_EMPTY_KEY):
        return {
            "success": False,
            "message": const.G_AUTHORIZATION_ERROR_MESSAGE,
            "data": None
        }

    pdf_checksum = get_pdf_file_checksum(contract.contract_pdf_file_path)
    #TODO ABI를 Call해서 이더리움에 contract_id : pdf_checksum 으로 기록되도록 실행
    contract.contract_auth = pdf_checksum
    contract.status_update()
    contract.update()

    return {
            "success": True,
            "message": "Consignor Sign Success",
            "data": None
        }


@app.get('/api/secret')
def secret_data(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    user = check_token(token)
    if user is None:
        return 'Abnormal Approach'
    return f'<h1>Secreter</h1>'


@app.post('/api/secret')
def secret_data_post(dummy: Model.LogoutModel, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    user = check_token(token)
    if user is None:
        return 'Abnormal Approach'
    return f'<h1>Secreter {dummy.id}</h1>'


@app.get('/api/dummy/contract')
def add_dummy_contract():
    contract_index = Contract.get_index()
    contract_id = generate_contract_id()
    user = User.select(index=1)[0]
    tar_json_path = os.path.join(
            const.G_CONTRACT_SAVE_FOLDER_PATH,
            const.G_CONTRACT_TYPE_LIST[0],
            const.G_CONTRACT_JSON_FOLDER_NAME,
            contract_id + '.json'
        )
    copy_json(
        os.path.join(
            const.G_CONTRACT_FORM_DIR,
            const.G_CONTRACT_TYPE_LIST[0],
            const.G_CONTRACT_BASE_FORMAT_FILE_NAME
        ),
        tar_json_path
    )
    contract = Contract(contract_index, contract_id, const.G_CONTRACT_AUTH_EMPTY_KEY,
                        const.G_CONTRACT_TYPE_MAP['bill_of_lading'],
                        user.index, user.name, user.phone, const.G_CONTRACT_SIGN_EMPTY_KEY,
                        "consignee", "010-0000-0000", const.G_CONTRACT_SIGN_EMPTY_KEY, tar_json_path, None, get_date_string(), None,
                        const.G_CONTRACT_STATUS_MAP['created'], 0)
    contract.insert()

if __name__ == '__main__':
    uvicorn.run(f'main:app', port=3002, host="0.0.0.0", reload=True)