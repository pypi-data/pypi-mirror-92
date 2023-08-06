from flask import send_file

from mark_excel.normal_write import Write


class NormalWrite(Write):
    def __init__(self, mark_excel):
        self.mark_excel = mark_excel

    def save(self, local_path):
        """
        保存EXCEL文件
        :param local_path: 保存路径
        :return:
        """
        self.mark_excel.workbook.save(local_path)

    def create_sheet(self, title: str, index: int = 0):
        """
        新建一个sheet
        :param title: sheet标题
        :param index: sheet插入下标
        :return: 创建的sheet
        """
        return self.mark_excel.workbook.create_sheet(title, index)

    def merge_one_row(self, row_index, value, length, sheet=None):
        """
        合并写入一行
        :param row_index:要写入第几行，从1开始计数
        :param value:写入的值
        :param length:合并单元格数量
        :param sheet:要操作的sheet,默认第一个sheet
        :return:
        """
        if sheet is None:
            sheet = self.mark_excel.workbook.worksheets[0]
        # 合并一行中的几个单元格
        sheet.merge_cells('A{}:{}{}'.format(row_index, self.mark_excel.LINE[length - 1], row_index))
        sheet.cell(row_index, 1).value = value
        sheet.row_dimensions[row_index].height = self.mark_excel.height
        sheet['A{}'.format(row_index)].alignment = self.mark_excel.align

    def one_row(self, row_index, alist, sheet=None):
        """
        正常情况下 写入一行数据
        :param row_index: 要写入第几行，从1开始计数
        :param alist: 要写入的数组
        :param sheet:要写入的sheet,默认第一个sheet
        :return:
        """
        if sheet is None:
            sheet = self.mark_excel.workbook.worksheets[0]
        # 首先设置一下这一行的高度
        sheet.row_dimensions[row_index].height = self.mark_excel.height
        for i, x in enumerate(alist):
            # 将数据写入指定单元格
            sheet.cell(row_index, i + 1).value = x
            # 设置该列的宽度
            sheet.column_dimensions[self.mark_excel.LINE[i]].width = self.mark_excel.width
            # 设置该列的对齐方式
            sheet['{}{}'.format(self.mark_excel.LINE[i], row_index)].alignment = self.mark_excel.align

    def merge(self, start_line, end_line, start_col, end_col, value, sheet=None):
        """
        合并行或者列
        :param start_line: 合并开始行
        :param end_line: 合并开始行
        :param start_col: 合并开始行
        :param end_col: 合并开始行
        :param value: 单元格值
        :param sheet: 要操作的sheet,默认第一个sheet
        :return:
        """
        if sheet is None:
            sheet = self.mark_excel.workbook.worksheets[0]
        sheet.merge_cells(value, start_line, start_col, end_line, end_col)
