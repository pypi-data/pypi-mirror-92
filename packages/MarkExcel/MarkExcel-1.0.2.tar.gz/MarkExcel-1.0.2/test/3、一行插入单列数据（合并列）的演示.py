from mark_excel import MarkExcel

me = MarkExcel()
me.write.merge_one_row(3, "第三行合并8列", 8)
me.write.save("3.xlsx")
