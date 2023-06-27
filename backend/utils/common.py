def get_diff_and_color(actual_value: str, prev_value: str):
    actual_domains: list[str] = actual_value.split(",")
    prev_domains: list[str] = prev_value.split(",")
    diff: int = len(actual_domains) - len(prev_domains)
    diff_str: str = f"+{diff}" if diff > 0 else str(diff)
    color: str = "green" if diff_str.startswith("-") or diff_str[0].isdigit() else "red"
    return diff_str, color
