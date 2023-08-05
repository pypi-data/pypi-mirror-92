movie=["第一滴血", "勇敢的心","教授与疯子",["我和我的祖国","战狼"]]
def print_lol(the_list):
 for each_item in the_list:
  if isinstance(each_item,list):
   print_lol(each_item)
  else:
   print(each_item)
