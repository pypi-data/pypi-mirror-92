#-*-coding:utf-8-*-


def flatten(nested):
    '''多层迭代输出
    '''
    try:
        #不要迭代类似字符串的对象,字符串本身是列表
        try:
            nested + ''
        except:
            pass
        else:
            raise TypeError
        for sublist in nested:
            for ele in flatten(sublist):
                yield ele
    except TypeError as tx:
        yield nested