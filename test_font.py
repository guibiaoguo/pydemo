# coding=utf-8
from fontTools.ttLib import TTFont

world = TTFont('font.ttf')
# 读取响应的映射关系
uni_list = world['cmap'].tables[0].ttFont.getGlyphOrder()  # 'cmap' 表示汉字对应的映射 为unicode编码
print(uni_list) # 按顺序拿到各个字符的unicode编码
unicode_list= [eval(r"u'\u" + uni[3:] + "'") for uni in uni_list[2:]]
unicode_list= [uni.encode('utf-8').decode('unicode-escape') for uni in unicode_list]
print('unicode_list = ', unicode_list)

font = TTFont('font.ttf')    # 打开文件
font.saveXML('font.xml')    # 保存为xml文件
