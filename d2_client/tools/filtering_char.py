
def automatic_filtering_invisible_char(string):
    """
    :param string:
    :return:
    """
    # 吸收不可见字符不应该放在这里
    return string.replace(' ', '').replace('\r', ' ').replace('\t', '').replace('\n', '')
