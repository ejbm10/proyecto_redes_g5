def compare(old,new):
    a={x['name']:x for x in old or []}; b={x['name']:x for x in new}; out=[]
    for n in b.keys()&a.keys():
        if a[n]['oper_status']!=b[n]['oper_status']: out.append((n,'oper_status_changed'))
        if a[n]['input_errors'] is not None and b[n]['input_errors'] is not None and b[n]['input_errors']>a[n]['input_errors']: out.append((n,'errors_increased'))
    return out
