def dict_to_query_params(d: dict):
    NULL_VALUES = ['', None]
    if not d:
        return ''
    q_params = '?'
    for k, v in d.items():
        if v not in NULL_VALUES:
            q_params += f"{k}={v}&"
    return q_params.rstrip("&") if len(q_params) > 1 else ''


def truncate_if_necessary(s, limit):
    s = str(s)
    return f'{s:.{limit}}...[{len(s) - limit} chars more]' if len(s) > limit else s
