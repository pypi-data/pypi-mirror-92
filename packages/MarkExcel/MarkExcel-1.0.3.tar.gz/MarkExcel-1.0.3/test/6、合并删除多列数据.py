from mark_excel import MarkExcel, MarkMergeExcel

me = MarkMergeExcel()

alist = []

for x in range(5):
    alist.append(x)
me.write.one_row(0, alist)
me.write.one_row(1, alist)
me.write.one_row(2, alist)
me.write.one_row(3, alist)
me.write.one_row(4, alist)
me.write.merge(2, 3, 1, 3, "Merge")
me.write.save("6.xlsx")
