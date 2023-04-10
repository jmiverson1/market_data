from multiprocessing import Pool

txt = [
    "  the text  in this is a  mess",
    "a lot of text data  is really messy "
]

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
    return output

if __name__ == '__main__':
    p = Pool(3)
    print(p.apply(func, (txt,)))