
def get_lfm(last_name: str, first_name: str = None, middle_name: str = None) -> str:
    """Из фаМиЛИя иМя ОтчЕство возвращает Фамилия И.О."""
    result = ''
    if last_name:
        result = last_name.capitalize()
        if first_name:
            result += ' ' + first_name[0].upper() + '.'
            if middle_name:
                result += middle_name[0].upper() + '.'
    return result


def get_fml(last_name: str, first_name: str = None, middle_name: str = None) -> str:
    """Из фаМиЛИя иМя ОтчЕство возвращает И.О. Фамилия"""
    result = ''
    if last_name:
        if first_name:
            result = first_name[0].upper() + '.'
            if middle_name:
                result += middle_name[0].upper() + '. ' + last_name.capitalize()
    return result
