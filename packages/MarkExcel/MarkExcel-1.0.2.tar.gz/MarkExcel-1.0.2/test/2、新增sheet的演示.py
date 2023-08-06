# 默认实例化
from mark_excel import MarkExcel

me = MarkExcel(need_default_sheet=False)
me.write.create_sheet("m1", 0)
me.write.create_sheet("m2", 2)
me.write.create_sheet("m3", 1)
me.write.save("2.xlsx")
