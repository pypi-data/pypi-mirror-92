# 实例化

from mark_excel import MarkExcel
from openpyxl.styles import Font, colors, Border, Side, Alignment

# 默认实例化
me = MarkExcel()

# 定义高度
me = MarkExcel(height=30)

# 定义高度和宽度
me = MarkExcel(width=20)

# 定义字体
font = Font(name='等线', size=11, italic=False, color=colors.BLACK, bold=False)
me = MarkExcel(font=font)

# 定义对齐方式
me = MarkExcel(font=Alignment(horizontal='center', vertical='center', wrap_text=True))

# 定义边框
border = Border(left=Side(border_style='thin', color='000000'),
                right=Side(border_style='thin', color='000000'),
                top=Side(border_style='thin', color='000000'),
                bottom=Side(border_style='thin', color='000000'))
me = MarkExcel(border=border)

# 不使用默认的sheet
me = MarkExcel(need_default_sheet=False)
