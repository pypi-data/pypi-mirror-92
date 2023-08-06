from random import choices

default_charset = "0123456789abcdef"

def generate_id_solid(length: int = 32, charset: str = default_charset) -> str:
    return "".join(choices(charset, k=length))

def generate_id_split(length: int = 24, charset: str = default_charset, split_pattern: list = [6,10,6]) -> str:
    chars = generate_id_solid(length, charset)
    output = ""
    total = 0
    for n in split_pattern:
        while n != 0:
            output += chars[total]
            total += 1
            n -= 1
        output += "-"
    return output[:-1]
