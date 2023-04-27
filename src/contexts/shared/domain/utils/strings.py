import re


def camel_case_to_snake_case(value: str) -> str:
    ans = re.sub(r"(?<!^)(?=[A-Z])", "_", value).lower()
    return ans
