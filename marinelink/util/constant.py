import os

G_PROJECT_BASE_DIR = r'/home/testworks/Downloads/goldmoon/marinelink'
G_SRC_DIR_PATH = os.path.join(G_PROJECT_BASE_DIR)
G_DATA_DIR_PATH = os.path.join(G_SRC_DIR_PATH, 'data')
G_DATA_DB_DIR_PATH = os.path.join(G_DATA_DIR_PATH)

G_DATA_REVIEW_DIR_PATH = os.path.join(G_DATA_DIR_PATH, 'review')

# DB CONSTANT
G_DB_FILE_PATH = os.path.join(G_DATA_DB_DIR_PATH, 'marinelink.db')
G_DB_TIMEOUT_SEC = 30

G_CFG_DIR_PATH = os.path.join(G_SRC_DIR_PATH, 'cfg')
G_TABLE_CFG_DIR_PATH = os.path.join(G_CFG_DIR_PATH, 'table')

G_USER_TABLE_SCHEMA_FILE_PATH = os.path.join(G_TABLE_CFG_DIR_PATH, 'user.json')
G_CONTRACT_TABLE_SCHEMA_FILE_PATH = os.path.join(G_TABLE_CFG_DIR_PATH, 'contract.json')

G_AUTH_SECRETE_KET = os.getenv("APP_SECRET_STRING", "marine_link_비밀코드")

G_TOKEN_SEP_KEYWORD = "|@|"
G_PAD_SEP_KEYWORD = "@|pnq|@"

G_CONTRACT_STATUS_MAP = {
    'created': 10,
    'saved': 20,
    'before_checked': 30,
    'checked': 40,
    'done': 50
}
G_CONTRACT_TYPE_LIST = ['bill_of_lading']
G_CONTRACT_TYPE_MAP = {
    G_CONTRACT_TYPE_LIST[0]: 100
}

G_CONTRACT_FORM_DIR = os.path.join(G_CFG_DIR_PATH, 'contract')
G_CONTRACT_BASE_FORMAT_FILE_NAME = 'base_contract.json'
G_CONTRACT_BASE_EXCEL_FORMAT_FILE_NAME = 'base_contract_excel.xlsx'

G_CONTRACT_AUTH_EMPTY_KEY = 'AUTH_EMPTY'
G_CONTRACT_SIGN_EMPTY_KEY = 'SIGN_EMPTY'
G_CONTRACT_FILE_EMPTY_KEY = 'FILE_EMPTY'

G_CONTRACT_SAVE_FOLDER_PATH = os.path.join(G_DATA_DIR_PATH, 'contract')
G_CONTRACT_JSON_FOLDER_NAME = 'json'
G_CONTRACT_PDF_FOLDER_NAME = 'pdf'

G_COMPANY_TEXT = "MarineLink From AniB"

G_AUTHORIZATION_ERROR_MESSAGE = "Abnormal Approach"