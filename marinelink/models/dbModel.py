import sqlite3
import json
from abc import ABCMeta, abstractmethod
import util.constant as const
from util.io_util import load_json


class SqliteAdapter:
    db_path = const.G_DB_FILE_PATH
    print(db_path)
    @classmethod
    def create(cls, a_create_query):
        with sqlite3.connect(cls.db_path, timeout=const.G_DB_TIMEOUT_SEC) as db:
            cursor = db.cursor()
            cursor.execute(a_create_query)
            db.commit()

    @classmethod
    def select(cls, a_select_query, a_select_parameter=None):
        with sqlite3.connect(cls.db_path, timeout=const.G_DB_TIMEOUT_SEC) as db:
            cursor = db.cursor()
            cursor.execute(a_select_query, a_select_parameter)
            data = cursor.fetchall()
            db.commit()
        return data

    @classmethod
    def insert(cls, a_select_query, a_parameters):
        with sqlite3.connect(cls.db_path, timeout=const.G_DB_TIMEOUT_SEC) as db:
            cursor = db.cursor()
            cursor.execute(a_select_query, a_parameters)
            db.commit()

    @classmethod
    def update(cls, a_select_query, a_parameters=None):
        with sqlite3.connect(cls.db_path, timeout=const.G_DB_TIMEOUT_SEC) as db:
            cursor = db.cursor()
            cursor.execute(a_select_query, a_parameters)
            db.commit()

    @classmethod
    def delete(cls, a_select_query, a_parameters=None):
        with sqlite3.connect(cls.db_path, timeout=const.G_DB_TIMEOUT_SEC) as db:
            cursor = db.cursor()
            cursor.execute(a_select_query, a_parameters)
            db.commit()


class DataBaseModel(metaclass=ABCMeta):
    schema_path: str = ""
    schema = load_json(schema_path)
    db_adapter = SqliteAdapter()

    def __repr__(self):
        return str({prop_name: getattr(self, prop_name) for prop_name in self.schema['map'].values()})

    def __init__(self, a_index, *args, **kwargs):
        self.index = a_index

    @classmethod
    def from_row(cls, a_row):
        return cls(*a_row)

    @classmethod
    def create_table(cls):
        query = f"CREATE TABLE IF NOT EXISTS {cls.schema['name']}"
        schema_param = [*[f'{col_name} {col_schema}' for col_name, col_schema in cls.schema['schema'].items()], *cls.schema['relation']]

        schema_query = ', '.join(schema_param)
        query = f'{query} ( {schema_query} );'
        cls.db_adapter.create(query)

    @classmethod
    def get_index(cls):
        query = f"SELECT SEQ FROM SQLITE_SEQUENCE WHERE NAME=?"
        return int(cls.db_adapter.select(query, [cls.schema['name']])[0][0]) + 1

    @classmethod
    def _select(cls, **kwargs):
        print(cls.schema)
        col_list = ', '.join(list(cls.schema['schema'].keys()))
        where_query = []
        values = []
        for col_name, col_param in kwargs.items():
            if col_param is not None:
                where_query.append(f"{cls.schema['invert_map'][col_name]}=?")
                values.append(col_param)
        if len(where_query) == 0:
            raise ValueError("전체 선택은 지원하지 않습니다.")
        where_query = ' AND '.join(where_query)
        query = f"SELECT {col_list} FROM {cls.schema['name']} WHERE {where_query}"
        return cls.db_adapter.select(query, values)

    def insert(self):
        values = tuple(getattr(self, prop_name) for prop_name in self.schema['map'].values())
        question = ','.join(['?']*len(self.schema['map']))
        query = f"INSERT INTO {self.schema['name']}({','.join(self.schema['map'].keys())}) VALUES({question})"
        self.db_adapter.insert(query, values)

    def _update(self, **kwargs):
        set_query = []
        values = []
        for col_name, col_param in kwargs.items():
            if col_param is not None:
                set_query.append(f"{self.schema['invert_map'][col_name]} = ?")
                values.append(col_param)
        if len(set_query) == 0:
            raise ValueError("변화된 프로퍼티가 존재하지 않습니다.")
        set_query = ', '.join(set_query)
        query = f"UPDATE {self.schema['name']} SET {set_query} WHERE {self.schema['name']}_INDEX = {self.index}"
        self.db_adapter.update(query, values)
        self.update_property()


    @abstractmethod
    def update_property(self):
        raise NotImplementedError

    def update(self):
        update_parameter_dict = {}
        for prop_name in self.schema['map'].values():
            try:
                if getattr(self, prop_name) != getattr(self, '_prev_' + prop_name):
                    update_parameter_dict[prop_name] = getattr(self, prop_name)
            except AttributeError:
                pass
        return self._update(**update_parameter_dict)

    @classmethod
    @abstractmethod
    def select(cls, *args, **kwargs):
        raise NotImplementedError


class User(DataBaseModel):
    schema_path = const.G_USER_TABLE_SCHEMA_FILE_PATH
    schema = load_json(schema_path)

    def __init__(self, a_index, a_id, a_pwd, a_email, a_phone, a_name, a_token_key, a_email_auth, a_is_delete):
        self.id = a_id
        self.pwd = a_pwd
        self.email = a_email
        self.phone = a_phone
        self.name = a_name
        self.token_key = a_token_key
        self.email_auth = a_email_auth
        self.is_delete = a_is_delete

        self._prev_id = self.id
        self._prev_pwd = self.pwd
        self._prev_email = self.email
        self._prev_phone = self.phone
        self._prev_name = self.name
        self._prev_token_key = self.token_key
        self._prev_email_auth = self.email_auth
        self._prev_is_delete = self.is_delete
        super().__init__(a_index)

    @classmethod
    def select(cls, index=None, id=None, pwd=None, email=None, phone=None, name=None, token_key=None, email_auth=None, is_delete=0):
        selected_row = cls._select(index=index, id=id, pwd=pwd, email=email, phone=phone, name=name, token_key=token_key, email_auth=email_auth, is_delete=is_delete)
        return [cls.from_row(row) for row in selected_row]

    def update_property(self):
        self._prev_id = self.id
        self._prev_pwd = self.pwd
        self._prev_email = self.email
        self._prev_phone = self.phone
        self._prev_name = self.name
        self._prev_token_key = self.token_key
        self._prev_email_auth = self.email_auth
        self._prev_is_delete = self.is_delete


class Contract(DataBaseModel):
    schema_path = const.G_CONTRACT_TABLE_SCHEMA_FILE_PATH
    schema = load_json(schema_path)

    def __init__(self, a_index, a_contract_id, a_contract_auth, a_contract_type, a_consignor_index, a_consignor_name, a_consignor_phone,
                 a_consignor_sign, a_consignee_name, a_consignee_phone, a_consignee_sign, a_contract_json_file_path,
                 a_contract_pdf_file_path, a_create_date, a_contracted_date, a_status, a_is_delete):
        self.contract_id = a_contract_id  # PDF 파일 생성시 발급되는 ID
        self.contract_auth = a_contract_auth  # PDF 파일 hash number
        self.contract_type = a_contract_type
        self.consignor_index = a_consignor_index
        self.consignor_name = a_consignor_name
        self.consignor_phone = a_consignor_phone
        self.consignor_sign = a_consignor_sign
        self.consignee_name = a_consignee_name
        self.consignee_phone = a_consignee_phone
        self.consignee_sign = a_consignee_sign
        self.contract_json_file_path = a_contract_json_file_path
        self.contract_pdf_file_path = a_contract_pdf_file_path
        self.create_date = a_create_date
        self.contracted_date = a_contracted_date
        self.status = a_status
        self.is_delete = a_is_delete

        self._prev_contract_id = self.contract_id
        self._prev_contract_auth = self.contract_auth
        self._prev_contract_type = self.contract_type
        self._prev_consignor_index = self.consignor_index
        self._prev_consignor_name = self.consignor_name
        self._prev_consignor_phone = self.consignor_phone
        self._prev_consignor_sign = self.consignor_sign
        self._prev_consignee_name = self.consignee_name
        self._prev_consignee_phone = self.consignee_phone
        self._prev_consignee_sign = self.consignee_sign
        self._prev_contract_json_file_path = self.contract_json_file_path
        self._prev_contract_pdf_file_path = self.contract_pdf_file_path
        self._prev_create_date = self.create_date
        self._prev_contracted_date = self.contracted_date
        self._prev_status = self.status
        self._prev_is_delete = self.is_delete

        super().__init__(a_index)

    @classmethod
    def select(cls, index=None, contract_id=None, contract_auth=None, contract_type=None, consignor_index=None, consignor_name=None, consignor_phone=None,
               consignor_sign=None, consignee_name=None, consignee_phone=None, consignee_sign=None, contract_json_file_path=None,
               contract_pdf_file_path=None, create_date=None, contracted_date=None, status=None, is_delete=0):
        selected_row = cls._select(index=index, contract_id=contract_id, contract_auth=contract_auth, contract_type=contract_type,
                                   consignor_index=consignor_index, consignor_name=consignor_name, consignor_phone=consignor_phone,
                                   consignor_sign=consignor_sign, consignee_name=consignee_name,
                                   consignee_phone=consignee_phone, consignee_sign=consignee_sign,
                                   contract_json_file_path=contract_json_file_path, contract_pdf_file_path=contract_pdf_file_path,
                                   create_date=create_date, contracted_date=contracted_date,
                                   status=status, is_delete=is_delete,
                                   )
        return [cls.from_row(row) for row in selected_row]

    def update_property(self):
        self._prev_contract_id = self.contract_id
        self._prev_contract_auth = self.contract_auth
        self._prev_contract_type = self.contract_type
        self._prev_consignor_index = self.consignor_index
        self._prev_consignor_name = self.consignor_name
        self._prev_consignor_phone = self.consignor_phone
        self._prev_consignor_sign = self.consignor_sign
        self._prev_consignee_name = self.consignee_name
        self._prev_consignee_phone = self.consignee_phone
        self._prev_consignee_sign = self.consignee_sign
        self._prev_contract_json_file_path = self.contract_json_file_path
        self._prev_contract_pdf_file_path = self.contract_pdf_file_path
        self._prev_create_date = self.create_date
        self._prev_contracted_date = self.contracted_date
        self._prev_status = self.status
        self._prev_is_delete = self.is_delete

    def status_update(self):
        if self.contract_auth != const.G_CONTRACT_AUTH_EMPTY_KEY:
            self.status = const.G_CONTRACT_STATUS_MAP['done']
        elif self.consignee_sign == const.G_CONTRACT_SIGN_EMPTY_KEY and self.consignor_sign == const.G_CONTRACT_SIGN_EMPTY_KEY:
            self.status = const.G_CONTRACT_STATUS_MAP['saved']
        elif self.consignee_sign == const.G_CONTRACT_SIGN_EMPTY_KEY or self.consignor_sign == const.G_CONTRACT_SIGN_EMPTY_KEY:
            self.status = const.G_CONTRACT_STATUS_MAP['checked']
        else:
            self.status = const.G_CONTRACT_STATUS_MAP['checked']

if __name__ == '__main__':
    # print(User.create_table())
    user1 = User(0, 'id', 'pwd', "email", "phone", "name", None, 0, 0)
    # user1.insert()
    print(User.select(is_delete=0))
    print(User.select(id='id'))
    print(User.select(id='none'))
    # print(Contract.create_table())
    contract1 = Contract(0, 'id', 'auth', 'type', 0, 'consignor_name', 'consignor_phone', 'consignor_sign', 'consignee_name',
                         'consignee_phone', 'consignee_sign', 'contract_json_path', 'contract_pdf_path', "2021-11-03 10:00:00", None, 'status', 0)
    # contract1.insert()
    print(Contract.select(index=0))
    print(Contract.select(consignee_name='consignee_name'))
