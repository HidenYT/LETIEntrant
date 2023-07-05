# LETIEntrant
Django-сервер для конвертации данных, передаваемых в запросе. Конвертация осуществляется из формата JSON в заданный XML формат, и наоборот.

## Запуск
Для запуска данного приложения необходимо предварительно установить:
- Python >= 3.9
- Django >= 4.2
- Библиотеку lxml для работы с XML форматом
- Библиотеку requests для отправки запросов

Для запуска проекта откройте командную строку в корневой папке проекта и введите команду:
```
python manage.py migrate
```
После этого введите команду:
```
python manage.py runserver
```
После последней команды приложение будет запущено (по умолчанию на порте 8000). Для открытия приложения перейдите в браузере по ссылке: http://localhost:8000/.

В файле settings.py корневого каталога проекта можно изменить значение параметра XML_VALIDATION. Если вам необходимо, чтобы сервер проверял исходящие и входящие XML файлы по представленным XSD схемам, установите XML_VALIDATION в значение True. В противном случае установите в значение False. 

## Использование
Конвертация из формата JSON в формат XML осуществляется по адресу:
http://localhost:8000/converter/jsontoxml/
с помощью POST запросов.


Конвертация из формата XML в формат JSON осуществляется по адресу:
http://localhost:8000/converter/xmltojson/
с помощью POST запросов.

Вы можете отправлять запросы на данные адреса с использованием curl или других средств. Перед отправкой запроса необходимо убедиться, что отправляемые данные находятся в кодировке UTF-8. При получении ответа от сервера также стоит перевести ответ в кодировку UTF-8. 

Для удобства отправки запросов была создана главная страница приложения (http://localhost:8000/). На ней вы можете отправить запрос на сервер с помощью графического интерфейса. В поле "Text" необходимо ввести текст XML или JSON файла, а в поле "File format choice" необходимо выбрать формат передаваемого вами файла (XML или JSON). Данная страница отправляет запрос на сервер так, будто это делает сторонее приложение, через библиотеку requests в Python.

## Заметки
В исходном файле формата JSON не было обнаружено полей для указания оснований для получения бесплатного образования. Поэтому в JSON файл были добавлены 2 поля: "free_eductaion_reason_id" и "free_eductaion_reason_oksm_id".

Также стоит отметить, что в XML файлах в разделе с адресами неизвестен формат поля для полного адреса. Соответственно, непонятно, как записывать адрес в это поле, и наоборот, как из этого поля считывать части адреса. Поэтому было решено, что в само поле с полным адресом будут через запятую без пробелов записаны поля: address_txt1,address_txt2,address_txt3,address_txt4,street,house,building,letter,building2,flat,post_index. И считываться при конвертации из XML в JSON, соответственно, поля будут в том же порядке и количестве.

## Примеры файлов для конвертации

<details>
  <summary>Пример JSON файла для конвертации в XML</summary>

```json
{
  "id": 32115,
  "user_id": 3878,
  "first_name": "Максим",
  "second_name": "Яруллин",
  "middle_name": null,
  "dict_sex_id": 1,
  "birthday": "07.08.2005",
  "citizenship_id": 185,
  "motherland": "Россия Г.Астана",
  "email": "mail@etu.ru",
  "tel_mobile": "+7 (888) 888-88-88",
  "tel_mobile_frn": "88888888888",
  "residence_country_id": 185,
  "kladr_1": "2200000000000",
  "kladr_2": "2200300000000",
  "kladr_3": "2200000100000",
  "kladr_4": "2200300002500",
  "address_txt1": "Могилевская область",
  "address_txt2": null,
  "address_txt3": null,
  "address_txt4": null,
  "street": null,
  "house": null,
  "building": null,
  "letter": null,
  "building2": null,
  "flat": null,
  "post_index": "111111",
  "has_another_living_address": false,
  "second_residence_country_id": 185,
  "second_kladr_1": null,
  "second_kladr_2": null,
  "second_kladr_3": null,
  "second_kladr_4": null,
  "second_address_txt1": null,
  "second_address_txt2": null,
  "second_address_txt3": null,
  "second_address_txt4": null,
  "second_street": null,
  "second_house": null,
  "second_building": null,
  "second_letter": null,
  "second_building2": null,
  "second_flat": null,
  "second_post_index": "111111",
  "passport_type_id": 1,
  "passport_series": "5661",
  "passport_number": "111111",
  "passport_begda": "08.9.2019",
  "passport_endda": null,
  "passport_org_code": "111-111",
  "passport_issued_by": "МВД-АВОР.ПРДЛПАРОДАЬЕК",
  "has_old_passport": true,
  "old_passport_type_id": null,
  "old_passport_series": null,
  "old_passport_number": "1111111",
  "old_passport_begda": "11.11.1111",
  "old_passport_endda": null,
  "old_passport_org_code": null,
  "old_passport_issued_by": null,
  "paid_by_another_human": null,
  "paid_passport_type_id": null,
  "paid_passport_series": null,
  "paid_passport_number": null,
  "paid_passport_begda": null,
  "paid_passport_endda": null,
  "paid_passport_org_code": null,
  "paid_passport_issued_by": null,
  "foreign_language_id": null,
  "need_hostel": null,
  "special_conditions": null,
  "is_with_disabilities": null,
  "institution_country_id": 185,
  "institution_city_id": null,
  "institution_city_text": null,
  "diploma_series": "123132",
  "diploma_number": "1211221",
  "diploma_date": "10.10.2000",
  "diploma_registration_number": "уц",
  "graduated_university_id": null,
  "has_not_found_university": null,
  "graduated_university_text": "кцу",
  "average_diploma_grade": null,
  "graduated_school_id": null,
  "has_not_found_school": null,
  "graduated_school_text": null,
  "edu_direction_id": null,
  "has_not_found_direction": null,
  "edu_direction_text": null,
  "has_no_same_level_diploma": false,
  "dict_bak_exam_reason_id": 4,
  "has_essay": true,
  "dict_asp_science_curators_id": null,
  "exam_foreign_language_id": null,
  "created_at": "2022-06-09T18:25:23.000000Z",
  "updated_at": "2023-03-05T10:12:29.000000Z",
  "created_by": 3878,
  "campaign_id": 4,
  "dict_edu_diploma_level_id": 4,
  "dict_edu_diploma_sublevel_id": 1,
  "dict_edu_diploma_name_id": 6,
  "edu_diploma_name_text": null,
  "application_scan_id": null,
  "uploaded_at": null,
  "applied_at": null,
  "revoked_at": null,
  "accepted_at": null,
  "denied_at": null,
  "dict_deny_reason_type_id": null,
  "deny_reason": null,
  "denied_by": null,
  "first_name_en": "Maxim",
  "second_name_en": "Yarullin",
  "middle_name_en": null,
  "has_no_street": true,
  "has_no_house": true,
  "has_no_second_street": false,
  "has_no_second_house": false,
  "bak_exam_wish_math": false,
  "bak_exam_wish_phys": false,
  "bak_exam_wish_rus": false,
  "bak_exam_wish_inf": false,
  "bak_exam_wish_eng": false,
  "bak_exam_wish_soc": false,
  "bak_exam_wish_chem": false,
  "has_without_exam_wish": true,
  "has_special_rights_wish": true,
  "has_priority_wish": true,
  "has_target_wish": true,
  "file_number": null,
  "is_locked": false,
  "locked_by": null,
  "applied_by": 3878,
  "revoked_by": null,
  "accepted_by": null,
  "snils": null,
  "locked_at": null,
  "revision": 1,
  "previous_application_id": null,
  "has_compatriot_wish": false,
  "is_compatriot": false,
  "has_ministry_line_wish": false,
  "is_ministry_line": false,
  "ministry_line_doc_name": null,
  "ministry_line_doc_number": null,
  "ministry_line_doc_date": null,
  "is_regrade_allowed": false,
  "idk_id": null,
  "tel_house": null,
  "is_foreigner": false,
  "is_paid": false,
  "paid_contract_num": null,
  "paid_contract_begda": null,
  "paid_contract_endda": null,
  "is_without_citizenship": false,
  "old_first_name": "Максим",
  "old_second_name": "Яруллин",
  "old_middle_name": null,
  "epgu_snils": null,
  "dict_document_return_id": 1,
  "epgu_achievement_sum": null,
  "dict_hostel_group_id": null,
  "is_first_settle_in_hostel": null,
  "dict_hostel_id": null,
  "is_send_to_sberbank": null,
  "is_sign_for_sberbank": null,
  "personal_number": null,
  "individual_number": null,
  "student_number": null,
  "mmiis_id": null,
  "is_sent_to_mmiis": false,
  "passport_name_text": null,
  "has_original_edu_diploma": false,
  "personal_data_consent_scan_id": null,
  "edu_kladr_1": "7800000000000",
  "edu_kladr_2": null,
  "edu_kladr_3": null,
  "edu_kladr_4": null,
  "edu_address_txt1": null,
  "edu_address_txt2": null,
  "edu_address_txt3": null,
  "edu_address_txt4": null,
  "is_online_bak_exam": false,
  "is_hidden_from_public_lists": false,
  "service_entrant_guid": null,
  "has_special_wish": false,
  "is_applied_offline": false,
  "photo_id": null,
  "passport_uuid": "151ad3fc-756f-46d0-8ec0-9d0355ec693a",
  "is_from_epgu": false,
  "is_applied_by_post": false,
  "is_russian_citizen_after_2022": false,
  "is_without_snils": true,
  "edu_document_uuid": "a06d0356-9997-4efe-86c0-a3348bd8b2f7",
  "is_passport_checked": false,
  "additional_files_added_at": null,
  "additional_files_checked_at": null,
  "has_additional_files": false,
  "is_additional_files_checked": false,
  "passport_epgu_id": null,
  "send_to_epgu": false,
  "is_education_document_checked": false,
  "edu_document_epgu_id": null,
  "original_edu_diploma_applied_at": null,
  "original_edu_diploma_revoked_at": null,
  "edu_document_uuid_2": "fc6ced9d-9925-4f88-aff7-279788c93829",
  "dict_mark_id": null,
  "has_epgu_original_education_document": false,
  "additional_tel_mobile": null,
  "step_navigation": 5,
  "public_code": "870-074-745 12",
  "free_eductaion_reason_id": null,
  "free_eductaion_reason_oksm_id": null
}
```
  
</details>

<details>
    <summary>Пример XML файла для конвертации в JSON</summary>

```XML
<?xml version="1.0" encoding="UTF-8"?>
<PackageData>
   <IdJwt>109940</IdJwt>
   <EntityAction>Campaign_Add</EntityAction>
   <SuccessResultList>
      <Entrant>
         <IdObject>309401</IdObject>
         <Guid>1234567890</Guid>
         <Snils>78487874890</Snils>
         <IdGender>1</IdGender>
         <Birthday>2002-01-01</Birthday>
         <Birthplace>Петропавловск-Камчатский</Birthplace>
         <Phone>89123456789</Phone>
         <Email>dbs@t.net</Email>
         <AvailabilityEduDoc>true</AvailabilityEduDoc>
         <DateAvailabilityEduDoc>2006-01-02T15:04:05+03:00</DateAvailabilityEduDoc>
         <Surname>Михалков</Surname>
         <Name>Степан</Name>
         <Patronymic>Евгеньевич</Patronymic>
         <IdOksm>185</IdOksm>
         <FreeEducationReason>
            <IdFreeEducationReason>2</IdFreeEducationReason>
            <IdOksmFreeEducationReason>100</IdOksmFreeEducationReason>
         </FreeEducationReason>
         <AddressList>
            <Address>
               <IsRegistration>1</IsRegistration>
               <FullAddr>Санкт-Петербург,,,,Греческий проспект,1,1,1,1,1,1</FullAddr>
               <IdRegion>4700000000000</IdRegion>
               <City>г. Санкт-Петербург</City>
            </Address>
         </AddressList>
         <DocumentList>
            <Document>
               <Guid>1413413654645</Guid>
               <FileHash>1100100010001010</FileHash>
               <IdDocumentType>1</IdDocumentType>
               <DocName>Паспорт гражданина Российской Федерации</DocName>
               <DocSeries>1234</DocSeries>
               <DocNumber>567890</DocNumber>
               <IssueDate>2010-01-01</IssueDate>
               <DocOrganization>Организация</DocOrganization>
               <IdCheckStatus>1</IdCheckStatus>
            </Document>
         </DocumentList>
         <Photo>
            <FileHash>19901809401010</FileHash>
            <Fui>aw04v84vi4j49g40</Fui>
         </Photo>
      </Entrant>
   </SuccessResultList>
</PackageData>
```
</details>