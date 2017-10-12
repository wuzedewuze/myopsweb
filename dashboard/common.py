# coding:utf-8

# 将forms返回的errors.as_data()返回值的内容取出

def get_errors_message(data):
    errdic = []
    for msg_exceptions in data.values():
        for msg in msg_exceptions:
            errdic.append(msg.args[0])
    print(errdic)
    errmsg = " and ".join(str(s) for s in errdic )
    return errmsg
