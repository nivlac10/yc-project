# byte转str
def bytes_to_str(date_list):
    if date_list:
        if type(date_list) == list:
            for date in date_list:
                for key in date.keys():
                    if type(date[key]) == bytes:
                        date[key] = bytes.decode(date[key])
        else:
            for key in date_list.keys():
                if type(date_list[key]) == bytes:
                    date_list[key] = bytes.decode(date_list[key])
    return date_list