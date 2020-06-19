def get_phone_display_format(phone_number):
    phone_string = str(phone_number)
    if len(phone_string) != 10:
        return phone_string
    return '(' + phone_string[0:3] + ') ' \
           + phone_string[3:6] + '-' + phone_string[6:]


def get_phone_save_format(phone_string):
    phone_string = str(phone_string)
    phone_number = ''
    for i in range(len(phone_string)):
        char = phone_string[i]
        if '0' <= char <= '9':
            phone_number += char
    return phone_number

    # print(phone_string)
    # print(type(phone_string))
    # return int(str(filter(str.isdigit, str(phone_string))))
