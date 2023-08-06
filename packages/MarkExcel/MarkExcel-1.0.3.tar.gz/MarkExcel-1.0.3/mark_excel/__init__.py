import xlwt
from openpyxl import Workbook
from openpyxl.styles import Font, colors, Alignment, Border, Side

from mark_excel.merge_write import MergeWrite
from mark_excel.read import Read
from mark_excel.write import Write, NormalWrite


class MarkExcel(object):
    def __init__(self, height=30, width=20, font=None, align=None, border=None, need_default_sheet=True):
        """
        实例化
        :param height: 单元格高度
        :param width: 单元格宽带
        :param font: 字体
        :param align: 对齐方式
        :param border: 边框
        :param need_default_sheet: 是否需要默认的sheet
        """
        # height：单元格的高度
        self.height = height
        # width：单元格的宽度
        self.width = width
        # 字体设置
        self.font = font if font else Font(name='等线', size=11, italic=False, color=colors.BLACK, bold=False)
        # 是否居中显示
        self.align = align if align else Alignment(horizontal='center', vertical='center', wrap_text=True)
        # 边框设置
        self.border = border if border else Border(left=Side(border_style='thin', color='000000'),
                                                   right=Side(border_style='thin', color='000000'),
                                                   top=Side(border_style='thin', color='000000'),
                                                   bottom=Side(border_style='thin', color='000000'))

        self.LINE = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                     "T", "U", "V", "W", "X", "Y", "Z"]
        # excel对象
        self.workbook = Workbook()
        # 是否需要默认的sheet
        if not need_default_sheet:
            # 不需要就删除
            self.workbook.remove(self.workbook.worksheets[0])
        # 写入对象
        self.write = NormalWrite(self)
        # 读取对象
        self.read = Read(self)


class MarkMergeExcel(object):
    def __init__(self, need_default_sheet=True):
        """
        实例化
        :param need_default_sheet: 是否需要默认的sheet
        """
        self.LINE = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                     "T", "U", "V", "W", "X", "Y", "Z"]
        # excel对象
        self.workbook = xlwt.Workbook()
        # 是否需要默认的sheet
        if need_default_sheet:
            # 不需要就删除
            self.workbook.add_sheet("sheet",cell_overwrite_ok=True)
        # 写入对象
        self.write = MergeWrite(self)
        # 读取对象
        self.read = Read(self)
