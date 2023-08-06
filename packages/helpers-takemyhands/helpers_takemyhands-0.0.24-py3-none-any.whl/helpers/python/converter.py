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


def year_digit_two_to_four(year):
    return f"19{year}" if int(year) > 21 else f"20{year}"


def six_digit_date_to_dict(date):
    if len(date) == 6:
        try:
            year = year_digit_two_to_four(date[:2])
            month = date[2:4]
            day = date[4:]
            return {
                "year": year,
                "month": month,
                "day": day,
            }
        except Exception as e:
            raise Exception(e)
    else:
        return f"hey, date does not 6 digit, i got {len(date)} digit."
