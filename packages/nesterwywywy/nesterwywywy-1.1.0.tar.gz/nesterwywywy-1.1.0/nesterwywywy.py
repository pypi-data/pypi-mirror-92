movie=["第一滴血", "勇敢的心","教授与疯子",["我和我的祖国",["送你一朵小红花","缉凶","拆弹专家3"],"战狼"]]
def print_lol(the_list,level):
 for each_item in the_list:
  if isinstance(each_item,list):
   print_lol(each_item,level+1)
  else:
   for tap_stop in range(level):
       print('\t',end='')
   print(each_item)
