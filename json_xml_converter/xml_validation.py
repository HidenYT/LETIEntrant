from lxml import etree
import os

JSON_TO_XML_MODE = 'jsontoxml'
XML_TO_JSON_MODE = 'xmltojson'

def validate_xml(xml: str, mode: str):
    if mode == 'xmltojson':
        path = os.path.join('json_xml_converter', 'files', 'Get_Entrant_List.xsd')
        schema = open(path, encoding='utf8').read()
    elif mode == 'jsontoxml':
        path = os.path.join('json_xml_converter', 'files', 'Add_Entrant_List.xml')
        schema = open(path, encoding='utf8').read()
    else:
        raise ValueError('The mode should have one of the following values: {}'.format((JSON_TO_XML_MODE, XML_TO_JSON_MODE)))
    schema_root = etree.XML(bytes(schema, encoding='utf8'))
    schema = etree.XMLSchema(schema_root)
    parser = etree.XMLParser(schema = schema)
    etree.fromstring(xml, parser)