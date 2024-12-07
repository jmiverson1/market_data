def func(x: list) -> list:
    """

    :param x:
    :return:
    """
    output = []
    for txt_str in x:
        txt_str = txt_str.replace(" a ", "")
        txt_str = txt_str.replace(" the ", "")
        txt_str = txt_str.replace("  ", " ")
        txt_str = txt_str.strip()
        output.append(txt_str)
    Q.put(output)