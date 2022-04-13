from abc import ABCMeta, abstractmethod
from util import constant as const
import os
import xlwings as xw
import shutil
from util.string_util import get_date_string

class BasePdfGenerator(metaclass=ABCMeta):
    def __init__(self, contract_vo, contract_json):
        self.contract_vo = contract_vo
        self.contract_json = contract_json

    @abstractmethod
    def generate(self):
        raise NotImplementedError

    @abstractmethod
    def get_pdf_file_path(self):
        raise NotImplementedError


class BLPdfGenerator(BasePdfGenerator):
    TYPE_KEYWORD = const.G_CONTRACT_TYPE_LIST[0]
    TYPE_CODE = const.G_CONTRACT_TYPE_MAP[TYPE_KEYWORD]

    def __init__(self, contract_vo, contract_json):
        super().__init__(contract_vo, contract_json)
        self.base_file_path = os.path.join(const.G_CONTRACT_FORM_DIR, self.TYPE_KEYWORD, const.G_CONTRACT_BASE_EXCEL_FORMAT_FILE_NAME)
        self.target_file_path = os.path.join(
                const.G_CONTRACT_SAVE_FOLDER_PATH,
                self.TYPE_KEYWORD,
                const.G_CONTRACT_PDF_FOLDER_NAME,
                self.contract_vo.contract_id + '.pdf'
            )
        self.dummy_file_path = os.path.join(
                const.G_CONTRACT_SAVE_FOLDER_PATH,
                self.TYPE_KEYWORD,
                const.G_CONTRACT_PDF_FOLDER_NAME,
                self.contract_vo.contract_id + '.xlsx'
            )

    def generate(self):
        shutil.copy(self.base_file_path, self.dummy_file_path)
        xlsx_book = xw.Book(self.dummy_file_path)
        xl = xw.apps.active.api

        try:
            work_sheets = xlsx_book.sheets['선하증권']
            work_sheets['A5'].value = f"{self.contract_json['consignor']['name']} LOC : {self.contract_json['consignor']['location']}"
            work_sheets['A6'].value = f"TEL : {self.contract_json['consignor']['TEL']} FAX : {self.contract_json['consignor']['FAX']}"

            work_sheets['A8'].value = f"{self.contract_json['consignee']['name']} LOC : {self.contract_json['consignee']['location']}"
            work_sheets['A9'].value = f"TEL : {self.contract_json['consignee']['TEL']} FAX : {self.contract_json['consignee']['FAX']}"

            work_sheets['W4'].value = self.contract_json['bl_no']

            work_sheets['Q6'].value = self.contract_json['export_references']
            work_sheets['Q8'].value = self.contract_json['forwarding_agent_reference']
            work_sheets['Q10'].value = self.contract_json['point_and_country_of_origin']
            work_sheets['Q12'].value = self.contract_json['domestic_routing__export_instructions']
            work_sheets['Q14'].value = self.contract_json['onward_inland_routing']
            work_sheets['Q16'].value = self.contract_json['for_transshipment_to']
            work_sheets['Q18'].value = self.contract_json['final_destination']

            work_sheets['A11'].font.size = 5
            work_sheets['A11'].value = ','.join([self.generate_people_info(people_info) for index, people_info in enumerate(self.contract_json['notify_party']) if index % 2 == 0])
            work_sheets['A12'].font.size = 5
            work_sheets['A12'].value = ','.join([self.generate_people_info(people_info) for index, people_info in enumerate(self.contract_json['notify_party']) if index % 2 == 1])

            work_sheets['A14'].value = self.contract_json['pre_carriage_by']
            work_sheets['I14'].value = self.contract_json['place_of_receipt']
            work_sheets['A16'].value = self.contract_json['ocean_vessel']
            work_sheets['I16'].value = self.contract_json['port_of_loading']
            work_sheets['A18'].value = self.contract_json['port_of_discharge']
            work_sheets['I18'].value = self.contract_json['place_of_delivery']

            work_sheets['A22'].value = self.contract_json['marks_n_number']
            work_sheets['F22'].value = self.contract_json['no_of_count_or_pkgs']
            work_sheets['L22'].value = self.contract_json['description_of_pkgs_or_goods']
            work_sheets['V22'].value = self.contract_json['goods_weight']
            work_sheets['AA22'].value = self.contract_json['measurement']

            work_sheets['A28'].value = self.contract_json['freight_and_charges_revenue_tons_rate_per']
            work_sheets['G28'].value = self.contract_json['prepaid']
            work_sheets['K28'].value = self.contract_json['collect']

            work_sheets['S35'].font.size = 5
            work_sheets['S35'].value = self.contract_vo.contract_id
            work_sheets['S36'].value = get_date_string()
            work_sheets['S37'].value = const.G_COMPANY_TEXT
            xlsx_book.to_pdf(self.target_file_path)
        finally:
            xlsx_book.close()
            xl.Quit()
            os.remove(self.dummy_file_path)

    def get_pdf_file_path(self):
        return self.target_file_path

    @staticmethod
    def generate_people_info(people_info):
        return f"{people_info['name']} / {people_info['location']} / T {people_info['TEL']} / F {people_info['FAX']}"


def factoryModule(contract_vo, contract_json) -> BasePdfGenerator:
    if int(contract_vo.contract_type) == int(BLPdfGenerator.TYPE_CODE):
        return BLPdfGenerator(contract_vo, contract_json)
    else:
        raise BasePdfGenerator(contract_vo, contract_json)
