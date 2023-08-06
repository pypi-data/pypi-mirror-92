from flask import send_file

from mark_excel import Write


class MergeWrite(Write):
    def __init__(self, mark_merge_excel):
        self.mark_merge_excel = mark_merge_excel

    def save(self, local_path):
        """
        保存EXCEL文件
        :param local_path: 保存路径
        :return:
        """
        self.mark_merge_excel.workbook.save(local_path)

    def create_sheet(self, title: str, index: int = 0):
        """
        新建一个sheet
        :param title: sheet标题
        :param index: sheet插入下标
        :return: 创建的sheet,这里无效
        """
        return self.mark_merge_excel.workbook.add_sheet(title)

    def one_row(self, row_index, alist, sheet=None):
        """
        正常情况下 写入一行数据
        :param row_index: 要写入第几行，从1开始计数
        :param alist: 要写入的数组
        :param sheet:要写入的sheet,默认第一个sheet
        :return:
        """
        if sheet is None:
            print("self.mark_merge_excel.workbook", type(self.mark_merge_excel.workbook))
            sheet = self.mark_merge_excel.workbook.get_sheet(0)
        for i, value in enumerate(alist):
            sheet.write(row_index, i, value)

    def merge(self, start_line, end_line, start_col, end_col, value, sheet=None):
        if sheet is None:
            print("self.mark_merge_excel.workbook", type(self.mark_merge_excel.workbook))
            sheet = self.mark_merge_excel.workbook.get_sheet(0)
        sheet.write_merge(start_line, end_line, start_col, end_col, value)
