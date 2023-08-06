from flask import send_file


class Write(object):
    def save(self, local_path):
        pass

    def save_flask_response(self, local_path, file_name=None):
        """
        文件存储，同时返回Flask的接口Response对象
        :param local_path: 文件保存路径
        :param file_name: 文件名字，如果不传就按照local_path来解析
        :return:
        """
        if file_name is None:
            file_name = local_path.split("/")[-1]
        self.save(local_path)
        return send_file(local_path, attachment_filename=file_name,
                         as_attachment=True,
                         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
