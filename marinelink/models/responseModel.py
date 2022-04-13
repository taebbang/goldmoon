from pydantic import BaseModel
from typing import Any, List, Union


class ReturnResponseModel(BaseModel):
    success: bool
    message: str
    data: Any = None


class RegisterModel(BaseModel):
    id: str
    pwd: str
    email: str
    phone: str
    name: str


class LoginModel(BaseModel):
    id: str
    pwd: str


class LogoutModel(BaseModel):
    id: str

############  BILL OF LADING MODEL START ###############


class ContractPerson(BaseModel):
    name: str
    location: str
    TEL: str
    FAX: str


class ContrainerInfo(BaseModel):
    type: str
    container_id: str
    seal_label_id: str


class ProductInfo(BaseModel):
    container_type: str
    container_number: str
    item_package_unit: str
    package_unit_number: str


class GrossWeightInfo(BaseModel):
    unit: str
    value: str


class MeasurementInfo(BaseModel):
    unit: str
    value: str


class LadenOnBoardTheVesselInfo(BaseModel):
    date: str
    by: str


class CarrierSignatureInfo(BaseModel):
    qualification: str
    by: str


class BillOfLading(BaseModel):
    consignor: ContractPerson
    consignee: ContractPerson
    notify_party: List[ContractPerson]
    pre_carriage_by: str
    place_of_receipt: str
    ocean_vessel: str
    voyage_no: str
    flag: str
    place_of_delivery: str
    port_of_loading: str
    port_of_discharge: str
    for_transhipment_to_final_destination: str
    container_info: ContrainerInfo
    item_info: ProductInfo
    description_goods: str
    gross_weight: GrossWeightInfo
    measurement: MeasurementInfo
    additional_body_info: str
    freight_prepaid: str
    freight_n_charge: str
    revenue_tons: str
    revenue_tons_rate: str
    per_rate_unit: str
    prepaid: str
    collect: str
    freight_prepaid_at: str
    freight_payable_at: str
    place_of_issue: str
    no_of_original_bl: str
    date_of_issue: str
    laden_on_board_the_vessel: LadenOnBoardTheVesselInfo
    carrier_signature: CarrierSignatureInfo


############  BILL OF LADING MODEL END ###############

class ContractModel(BaseModel):
    type: str
    id: str
    # info: Union[BillOfLading, None] 에러가 나서 바꿈
    info: dict

class GetContractSignInfoModel(BaseModel):
    name: str
    phone: str

class ContractPersonSignModel(BaseModel):
    name: str
    phone: str

class RunContractModel(BaseModel):
    contract_id: str