from mark_excel import MarkExcel

me = MarkExcel()
me.write.one_row(2, [1, 2, 3, 4, 5, 6])
me.write.save("4.xlsx")
