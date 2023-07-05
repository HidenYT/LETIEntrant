from typing import Iterable, Callable
from django import views
from django import http
from django.core.exceptions import BadRequest, ValidationError
import json
from lxml import etree
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from . import xml_validation
from django.conf import settings
import os

class JSONtoXML(views.View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        path = os.path.join('json_xml_converter', 'files', 'dict_document_type_cls.json')
        self.doctype_cls = json.loads(open(path, encoding='utf8').read())
    
    def convert_date(self, str_date: str) -> str:
        dt = datetime.strptime(str_date, '%d.%m.%Y')
        return dt.strftime('%Y-%m-%d')

    def add_subelement_with_text(self, root: etree.Element, 
                                 name: str, 
                                 text: str) -> etree.Element:
        if text is not None:
            sub = etree.SubElement(root, name)
            if sub is not None:
                sub.text = str(text)
            return sub
        return None

    def find_document_by_id(self, id: int) -> Iterable:
        for doctype in self.doctype_cls:
            if doctype['Id'] == id:
                return doctype
        return None
    
    def generate_identificaiton_fields_from_json(self, 
                                                 json: dict, 
                                                 passport: Iterable
                                                 ) -> etree.Element:
        Fields = etree.Element('Fields')
        for field in passport['FieldsDescription']['fields']:
            field_name = field['xml_name']
            text = None
            if field_name == 'SubdivisionCode':
                if json['passport_org_code'] is None:
                    raise ValidationError('Inappropriate xml file generated')
                text = str(json['passport_org_code'])

            if field_name == 'IdOksm':
                if json['citizenship_id'] is None:
                    raise ValidationError('Inappropriate xml file generated')
                text = json['citizenship_id']

            if field_name == 'Surname':
                if json['second_name'] is None:
                    raise ValidationError('Inappropriate xml file generated')
                text = json['second_name']

            if field_name == 'Name':
                if json['first_name'] is None:
                    raise ValidationError('Inappropriate xml file generated')
                text = json['first_name']

            if field_name == 'Patronymic':
                text = json['middle_name']

            if field_name == 'ExpirationDate':
                text = json['passport_endda']

            if field_name == 'ProlongationDate':
                # TODO возможно, что это неправильно, поэтому возможно надо написать об этом в README и добавить соответствующее поле в json
                text = json['passport_endda']

            self.add_subelement_with_text(Fields, field_name, text)
        return Fields
    
    def generate_identification_from_json(self, json: dict) -> etree.Element:
        identification = etree.Element('Identification')

        passport_id = json['passport_type_id']
        passport = self.find_document_by_id(passport_id+100000)

        IdDocumentType = etree.SubElement(identification, 'IdDocumentType')
        IdDocumentType.text = str(passport_id)

        DocName = etree.SubElement(identification, 'DocName')
        DocName.text = str(passport['Name'])

        DocSeries = etree.SubElement(identification, 'DocSeries')
        DocSeries.text = str(json['passport_series'])

        DocNumber = etree.SubElement(identification, 'DocNumber')
        DocNumber.text = str(json['passport_number'])

        IssueDate = etree.SubElement(identification, 'IssueDate')
        IssueDate.text =  str(self.convert_date(json['passport_begda']))

        DocOrganization = etree.SubElement(identification, 'DocOrganization')
        DocOrganization.text =  str(json['passport_issued_by'])

        fields = self.generate_identificaiton_fields_from_json(json, passport)
        identification.append(fields)
        return identification

    def get_full_address(self, json: dict, prefix: str='') -> str:
        result = '{addr1},{addr2},{addr3},{addr4},{street},{house},{building},{letter},{building2},{flat},{post_index}'.format(
            addr1=json[prefix+'address_txt1'] or '',
            addr2=json[prefix+'address_txt2'] or '',
            addr3=json[prefix+'address_txt3'] or '',
            addr4=json[prefix+'address_txt4'] or '',
            street=json[prefix+'street'] or '',
            house=json[prefix+'house'] or '',
            building=json[prefix+'building'] or '',
            letter=json[prefix+'letter'] or '',
            building2=json[prefix+'building2'] or '',
            flat=json[prefix+'flat'] or '',
            post_index=json[prefix+'post_index'] or '',
        )
        return result

    def generate_address_list_from_json(self, json: dict) -> etree.Element:
        address_list = etree.Element('AddressList')
        reg_address = etree.SubElement(address_list, 'Address')
        self.add_subelement_with_text(reg_address, 'IsRegistration', 'true')
        self.add_subelement_with_text(reg_address, 'FullAddr', self.get_full_address(json))
        # TODO в README надо указать, что IsRegistration скорее должен быть не элементом, а атрибутом.
        self.add_subelement_with_text(reg_address, 'IdRegion', json['kladr_1'])
        self.add_subelement_with_text(reg_address, 'City', json['address_txt1'])

        if json['has_another_living_address']:
            liv_address = etree.SubElement(address_list, 'Address')
            self.add_subelement_with_text(liv_address, 'IsRegistration', 'false')
            self.add_subelement_with_text(liv_address, 'FullAddr', self.get_full_address(json, 'second_'))
            self.add_subelement_with_text(liv_address, 'IdRegion', json['second_kladr_1'])
            self.add_subelement_with_text(liv_address, 'City', json['second_address_txt1'])
        return address_list

    def generate_xml_from_json(self, json: dict) -> str:
        xml_parent = etree.Element('EntrantChoice')
        if json['service_entrant_guid']:
            self.add_subelement_with_text(xml_parent, 'Guid', json['service_entrant_guid'])
            return etree.tostring(xml_parent, xml_declaration=True, encoding='utf8', pretty_print=True)
        add_entrant = etree.SubElement(xml_parent, 'AddEntrant')
        identification = self.generate_identification_from_json(json)
        add_entrant.append(identification)

        if not json['is_without_snils']:
            self.add_subelement_with_text(add_entrant, 'Snils', json['snils'])
        
        self.add_subelement_with_text(add_entrant, 'IdGender', json['dict_sex_id'])
        self.add_subelement_with_text(add_entrant, 'Birthday', self.convert_date(json['birthday']))
        self.add_subelement_with_text(add_entrant, 'Birthplace', json['motherland'])
        self.add_subelement_with_text(add_entrant, 'Phone', json['tel_mobile'])
        self.add_subelement_with_text(add_entrant, 'Email', json['email'])
        self.add_subelement_with_text(add_entrant, 'IdOksm', json['citizenship_id'])

        if json['free_eductaion_reason_id'] is not None:
            FreeEducationReason = etree.SubElement(add_entrant, 'FreeEducationReason')
            self.add_subelement_with_text(FreeEducationReason, 'IdFreeEducationReason', json['free_eductaion_reason_id'])
            self.add_subelement_with_text(FreeEducationReason, 'IdOksmFreeEducationReason', json['free_eductaion_reason_oksm_id'])

        address_list = self.generate_address_list_from_json(json)
        add_entrant.append(address_list)
        
        return etree.tostring(xml_parent, xml_declaration=True, encoding='utf8', pretty_print=True)

    def post(self, request: http.HttpRequest) -> http.HttpResponse:
        if request.content_type != 'application/json':
            raise BadRequest('The content type must be application/json')
        json_data = json.loads(request.body)
        xml = self.generate_xml_from_json(json_data)

        if settings.XML_VALIDATION:
            try:
                xml_validation.validate_xml(xml, xml_validation.JSON_TO_XML_MODE)
            except:
                raise ValidationError('Inappropriate xml file generated')
        return http.HttpResponse(xml, content_type='text/xml')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class XMLtoJSON(views.View):
    def set_value(self, 
                  template: dict, 
                  json_tag: str, 
                  xml_element: etree.Element, 
                  subelement_tag: str, 
                  cast: Callable = str) -> None:
        subel = self.get_subelement(xml_element, subelement_tag)
        if subel is not None:
            template[json_tag] = cast(subel.text)

    def convert_date(self, date: str) -> str:
        dt = datetime.strptime(date, '%Y-%m-%d')
        return dt.strftime('%d.%m.%Y')

    def get_subelement(self, element: etree._Element, tag: str) -> etree._Element:
        for child in element:
            if child.tag == tag:
                return child
        return None
    
    def fill_address_fields(self, template: dict, Address: etree._Element, prefix: str='') -> None:
        parts = self.get_subelement(Address, 'FullAddr').text.split(',')
        template[prefix+'address_txt1'] = parts[0] or None
        template[prefix+'address_txt2'] = parts[1] or None
        template[prefix+'address_txt3'] = parts[2] or None
        template[prefix+'address_txt4'] = parts[3] or None
        template[prefix+'street'] = parts[4] or None
        template[prefix+'house'] = parts[5] or None
        template[prefix+'building'] = parts[6] or None
        template[prefix+'letter'] = parts[7] or None
        template[prefix+'building2'] = parts[8] or None
        template[prefix+'flat'] = parts[9] or None
        template[prefix+'post_index'] = parts[10] or None

    def fill_address_list(self, template: dict, Entrant: etree._Element) -> etree._Element:
        AddressList = self.get_subelement(Entrant, 'AddressList')
        template['has_another_living_address'] = False
        for Address in AddressList.getchildren():
            IsRegistration = self.get_subelement(Address, 'IsRegistration')
            is_reg_text = IsRegistration.text.lower()
            if is_reg_text == 'true' or is_reg_text == '1':
                self.fill_address_fields(template, Address)
            else:
                template['has_another_living_address'] = True
                self.fill_address_fields(template, Address, 'second_')
        return AddressList

    def fill_document_list(self, template: dict, Entrant: etree._Element) -> etree._Element:
        DocumentList = self.get_subelement(Entrant, 'DocumentList')
        if DocumentList is None: return
        for Document in DocumentList.getchildren():
            if self.get_subelement(Document, 'IdAchievementCategory') is not None:
                continue
            self.set_value(template, 'passport_type_id', Document, 'IdDocumentType', int)
            self.set_value(template, 'passport_series', Document, 'DocSeries')
            self.set_value(template, 'passport_number', Document, 'DocNumber')
            self.set_value(template, 'passport_begda', Document, 'IssueDate', self.convert_date)
            self.set_value(template, 'passport_issued_by', Document, 'DocOrganization')

    def fill_template(self, Entrant: etree.Element, template: dict) -> None:
        self.set_value(template, 'user_id', Entrant, 'IdObject', int)
        self.set_value(template, 'service_entrant_guid', Entrant, 'Guid')
        snls = self.get_subelement(Entrant, 'Snils')
        template['is_without_snils'] = (snls is None)
        if snls is not None: 
            template['snils'] = snls.text
        self.set_value(template, 'dict_sex_id', Entrant, 'IdGender', int)
        self.set_value(template, 'birthday', Entrant, 'Birthday', self.convert_date)
        self.set_value(template, 'motherland', Entrant, 'Birthplace')
        self.set_value(template, 'tel_mobile', Entrant, 'Phone')
        self.set_value(template, 'email', Entrant, 'Email')
        self.set_value(template, 'second_name', Entrant, 'Surname')
        self.set_value(template, 'first_name', Entrant, 'Name')
        self.set_value(template, 'middle_name', Entrant, 'Patronymic')
        self.set_value(template, 'citizenship_id', Entrant, 'IdOksm', int)

        FreeEducationReason = self.get_subelement(Entrant, 'FreeEducationReason')
        self.set_value(template, 'free_eductaion_reason_id', FreeEducationReason, 'IdFreeEducationReason', int)
        self.set_value(template, 'free_eductaion_reason_oksm_id', FreeEducationReason, 'IdOksmFreeEducationReason', int)
        
        self.fill_address_list(template, Entrant)
        
        self.fill_document_list(template, Entrant)

        Photo = self.get_subelement(Entrant, 'Photo')
        if Photo is not None:
            self.set_value(template, 'photo_id', Photo, 'Fui')

    def generate_json_from_xml(self, xml: str) -> str:
        path = os.path.join('json_xml_converter', 'files', 'json_template.json')
        json_template_text = open(path).read()
        result_json_list = []

        PackageData: etree.Element = etree.fromstring(xml)
        SuccessResultList = self.get_subelement(PackageData, 'SuccessResultList')
        if not SuccessResultList: return PackageData

        for Entrant in SuccessResultList.getchildren():
            template = json.loads(json_template_text)
            self.fill_template(Entrant, template)
            result_json_list.append(template)
        
        return result_json_list

    def post(self, request: http.HttpRequest):
        if request.content_type not in ('text/xml', 'application/xml'):
            raise BadRequest('The content type must be text/xml or application/xml')
        xml = request.body
        if settings.XML_VALIDATION:
            try:
                xml_validation.validate_xml(xml, xml_validation.XML_TO_JSON_MODE)
            except:
                raise ValidationError('Inappropriate xml file recieved')

        json_text = self.generate_json_from_xml(xml)

        return http.JsonResponse(json_text, safe=False, json_dumps_params={'indent': 4, 'ensure_ascii': False})
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)