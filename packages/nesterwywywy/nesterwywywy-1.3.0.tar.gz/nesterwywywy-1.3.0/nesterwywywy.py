movie=["第一滴血", "勇敢的心","教授与疯子",["我和我的祖国",["送你一朵小红花","缉凶","拆弹专家3"],"战狼"]]
def print_lol(the_list,indent=False,level=0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for tap_stop in range(level):
                    print('\t',end='')#也可以替换成为print('\t'*level,end='')
            print(each_item)
