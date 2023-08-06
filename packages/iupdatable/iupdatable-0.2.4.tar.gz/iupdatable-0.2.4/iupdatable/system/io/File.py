import os
import csv
import pathlib


class File(object):

    @staticmethod
    def read(file_path: str, encoding="utf_8_sig") -> str:
        """"
        读取文件
        :param file_path: 完整的文件路径
        :param encoding: 编码格式，默认utf_8_sig，这是Windows下记事本utf8的编码格式
        :return:
        """
        with open(file_path, encoding=encoding) as f:  # 默认为utf8编码
            return f.read()

    @staticmethod
    def write(file_path: str, content: str, encoding="utf_8_sig") -> None:
        """"
        写入文件
        :param file_path: 完整的文件路径
        :param content: 待写入内容
        :param encoding: 编码格式，默认utf_8_sig，这是Windows下记事本utf8的编码格式
        :return:
        """
        with open(file_path, "w", encoding=encoding) as f:
            f.write(content)

    @staticmethod
    def append(file_path: str, content: str, encoding="utf_8_sig") -> None:
        """"
        追加写入文件
        :param file_path: 完整的文件路径
        :param content: 待写入内容
        :param encoding: 编码格式，默认utf_8_sig，这是Windows下记事本utf8的编码格式
        :return:
        """
        with open(file_path, "a", encoding=encoding) as f:
            f.write(content)

    @staticmethod
    def append_new_line(file_path: str, content: str, encoding="utf_8_sig") -> None:
        """"
        新建一行，然后追加写入文件
        新文件或空白文件，则不添加新行
        :param file_path: 完整的文件路径
        :param content: 待写入内容
        :param encoding: 编码格式，默认utf_8_sig，这是Windows下记事本utf8的编码格式
        :return:
        """
        is_exist = os.path.exists(file_path)

        if is_exist:
            with open(file_path, "a", encoding=encoding) as file:
                size = os.path.getsize(file_path)
                if size == 3 and encoding.lower() == "utf_8_sig":  # utf_8_sig的txt文件会在开头添加三个字节的标识
                    file.write(content)
                elif size == 0 and encoding.lower() != "utf_8_sig":
                    file.write(content)
                else:
                    file.write("\n" + content)
        else:
            with open(file_path, "a", encoding=encoding) as new_file:
                new_file.write(content)

    @staticmethod
    def read_lines(file_path: str, remove_empty_line=True, remove_empty_space=True, encoding="utf_8_sig") -> []:
        """
        按行一次性读取文件
        :param file_path: 完整的文件路径
        :param remove_empty_line: 是否去除空白行
        :param remove_empty_space: 是否移除每行前后的空白
        :param encoding: 编码格式，默认utf_8_sig，这是Windows下记事本utf8的编码格式
        :return:
        """
        lines = []
        with open(file_path, encoding=encoding) as f:  # 默认为utf8编码
            for line in f.readlines():
                if remove_empty_space:
                    line = line.strip()
                if remove_empty_line:
                    line = line.rstrip('\n')  # 去掉每行的回车
                    if line:  # 去掉空行
                        lines.append(line)
                else:
                    line = line.rstrip('\n')  # 去掉每行的回车
                    lines.append(line)
        return lines

    @staticmethod
    def write_lines(file_path: str, lines: [], encoding="utf_8_sig") -> None:
        """
        按行一次性写入文件
        :param file_path: 完整的文件路径
        :param lines: 待写入的多行内容
        :param encoding: 编码格式，默认utf_8_sig，这是Windows下记事本utf8的编码格式
        :return:
        """
        with open(file_path, "w", encoding=encoding) as f:
            str_lines = [str(line) for line in lines]  # 针对数组中有数字的情况
            f.write('\n'.join(str_lines))

    @staticmethod
    def write_csv(file_path: str, rows: []) -> None:
        """
        写入CSV文件
        :param file_path: 完整的文件路径，如："D:\\12.csv","1.csv"
        :param rows: 待写入的多行数据，如：[['row11','row12','row13'],['row21','row22','row23']]
        :return:
        """
        with open(file_path, 'w', encoding='utf_8_sig', newline='') as f:
            csv_write = csv.writer(f)
            for oneRow in rows:
                csv_write.writerow(oneRow)

    @staticmethod
    def read_csv(file_path: str, encoding="utf_8_sig") -> []:
        """
        读取CSV文件
        :param file_path: 完整的文件路径，如："D:\\12.csv","1.csv"
        :param encoding: 文件编码，默认为utf_8_sig
        :return:
        """
        rows = []
        with open(file_path, 'r', encoding=encoding) as f:
            csv_reader = csv.reader(f)
            for oneRow in csv_reader:
                rows.append(oneRow)
        return rows

    @staticmethod
    def exist(file_path: str) -> bool:
        """
        检查一个文件是否存在
        :param file_path: 文件的路径
        :return: 有任意一种格式的存在即认为文件存在
        """
        if os.path.isfile(file_path):
            return True
        else:
            return False

    @staticmethod
    def exist_within_extensions(file_path: str, extension_list: []) -> bool:
        """
        检查一个文件是否存在（在指定的几种格式中）
        :param file_path: 文件的路径
        :param extension_list: 关心的格式,如：["jpg", "png", "bmp"]
        :return: 有任意一种格式的存在即认为文件存在
        """
        if os.path.isfile(file_path):
            return True
        win_path = pathlib.PureWindowsPath(file_path)
        file_path_no_extension = str(win_path.parent) + "\\" + win_path.stem
        for one_extension in extension_list:
            new_file_path = file_path_no_extension + "." + one_extension
            if os.path.isfile(new_file_path):
                return True
        return False

    @staticmethod
    def get_file_path_within_extensions(file_path: str, extension_list: []) -> str:
        """
        获取一个文件的路径（在指定的几种格式中）
        适用场景：
        想要获取一个指定路径下的文件，如：c:\testfile，
        但并不关心其具体是什么格式，只要是在extension_list指定的其中一种即可（靠前的优先）
        :param file_path: 文件的路径，如：c:\testfile，一个没有拓展名的文件（拓展名可有可无）
        :param extension_list: 关心的格式,如：["jpg", "png", "bmp"]
        :return: 不存在则返回None
        """
        if os.path.isfile(file_path):
            return file_path
        win_path = pathlib.PureWindowsPath(file_path)
        file_path_no_extension = str(win_path.parent) + "\\" + win_path.stem
        for one_extension in extension_list:
            new_file_path = file_path_no_extension + "." + one_extension
            if os.path.isfile(new_file_path):
                return new_file_path
        return None
