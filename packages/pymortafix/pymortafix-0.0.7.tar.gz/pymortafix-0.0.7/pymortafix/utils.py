from re import sub


def multisub(sub_dict, string):
    """Infinite sub in one iteration # sub_dict: {what_to_sub:substitution}"""
    rgx = "|".join(f"({s})" for s in sub_dict.keys())
    return sub(rgx, lambda m: sub_dict.get(m.group()), string)
