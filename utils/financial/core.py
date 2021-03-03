

def comma_decimal2float(foo: str):
    return float(foo.replace(".", "").replace(",", "."))


def dot_decimal2float(foo: str):
    return float(foo.replace(",", ""))
