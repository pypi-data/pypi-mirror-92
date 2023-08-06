from aishu import setting
def sql(key):
    """
    对应数据服务的sql语句注册
    :param key:
    :return:
    """
    switcher = {
        'UserID':{'sql':'select userId from User where loginName = "admin";',
                  'database':'AnyRobot'}
    }

    if switcher.get(key) is not None:
        if switcher[key].get('database') is not None:
            if len(switcher[key]['database']) == 0:
                setting.database = 'AnyRobot'
            else:
                setting.database = switcher[key]['database']

        return switcher[key]['sql']
    else:
        return False
