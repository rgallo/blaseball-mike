from blaseball_mike.session import session, check_network_response

BASE_URL = 'https://api.sibr.dev/eventually'

"""
Search through feed events.
Set to limit -1 to get everything. (warning: may take a while!)
Possible parameters for query: https://allie-signet.stoplight.io/docs/eventually/reference/eventually-api.v1.yaml/paths/~1events/get
"""
def search(cache_time=5, limit=100, query={}):
    s = session(cache_time)

    res = []
    res_len = 0

    while limit == -1 or res_len < limit:
        out = check_network_response(s.get(f"{BASE_URL}/events",params={'offset': res_len, 'limit': 100, **query}))
        out_len = len(out)
        if out_len < 100:
            res += out
            break
        else:
            res_len += out_len
            res += out

    return res

"""
Search through feed events.
Set to limit -1 to get everything. (warning: may take a while!)
Returns a generator that only gets the following page when needed.
"""
def lazy_search(cache_time=5, limit=100, query={}):
    s = session(cache_time)

    res_len = 0

    while limit == -1 or res_len < limit:
        out = check_network_response(s.get(f"{BASE_URL}/events",params={'offset': res_len, 'limit': 100, **query}))
        out_len = len(out)
        if out_len < 100:
            yield from out
            break
        else:
            res_len += out_len
            yield from out
