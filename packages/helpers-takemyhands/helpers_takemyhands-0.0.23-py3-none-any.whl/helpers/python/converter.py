# conver string to byte array
import xmltodict, json

def string_to_bytearray(string):
    if string is None:
        return None                    
    b = bytearray()
    b.extend(map(ord, string))
    return b


def string_to_dict(string):
    return xmltodict.parse(string)


def dict_to_json(dict):
    return json.dumps(dict)


def xml_to_json(xml):
    return json.loads(dict_to_json(string_to_dict(xml)))
