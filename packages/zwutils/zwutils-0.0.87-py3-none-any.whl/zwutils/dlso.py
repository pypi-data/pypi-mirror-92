'''
dict list set object utils
'''
class ZWObject(object):
    pass

def dict2obj(kv):
    kv = kv or {}
    # o = type('', (), {})()
    o = ZWObject()
    for key, val in kv.items():
        setattr(o, key, val)
    return o

def obj2dict(o):
    # o = o or type('', (), {})()
    o = o or ZWObject()
    r = {}
    attrs = [a for a in dir(o) if not a.startswith('_')]
    for attr in attrs:
        r[attr] = getattr(o, attr)
    return r

def tbl2dict(h, rs):
    '''h：表头list，rs：数据二维list。
    将每条数据（r）与表头按顺序匹配，形成dict list
    '''
    return [dict(zip(h, r)) for r in rs]

def extend_attrs(o, kv):
    '''
    Extend num of o's attrs, update o's attr's value by kv
    kv: dict/obj
    '''
    # o = o or type('', (), {})()
    o = o or ZWObject()
    kv = kv or {}
    o = dict2obj(o) if isinstance(o, dict) else o
    kv = obj2dict(kv) if not isinstance(kv, dict) else kv
    for key, val in kv.items():
        setattr(o, key, val)
    return o

def update_attrs(o, kv):
    '''
    Update o's attr's value by kv without add new attrs into o
    kv: dict/obj
    '''
    # o = o or type('', (), {})()
    o = o or ZWObject()
    kv = kv or {}
    o = dict2obj(o) if isinstance(o, dict) else o
    kv = obj2dict(kv) if not isinstance(kv, dict) else kv
    for key, val in kv.items():
        if hasattr(o, key):
            setattr(o, key, val)
    return o

def upsert_config(parent_cfg, default_cfg, new_cfg, param_cfg):
    '''
    param_cfg overwirte new_cfg overwirte default_cfg overwirte parent_cfg
    '''
    # pcfg = parent_cfg or type('', (), {})()
    pcfg = parent_cfg or ZWObject()
    dcfg = default_cfg or {}
    ncfg = new_cfg or {}
    pmcfg = param_cfg or {}
    pcfg = extend_attrs(pcfg, dcfg)
    pcfg = extend_attrs(pcfg, ncfg)
    pcfg = extend_attrs(pcfg, pmcfg)

    def change_nest_dict_to_obj(o):
        attrs = dir(o)
        attrs = [a for a in attrs if not a.startswith('_')]
        for attr in attrs:
            val = getattr(o, attr)
            if isinstance(val, dict):
                new_val = dict2obj(val)
                new_val = change_nest_dict_to_obj(new_val)
                setattr(o, attr, new_val)
        return o
    change_nest_dict_to_obj(pcfg)
    return pcfg

