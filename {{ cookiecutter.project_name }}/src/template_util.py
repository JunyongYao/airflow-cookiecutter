from IPython import get_ipython
import os


default_relative_output_path = "../data/output"


def is_notebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True  # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter


def get_notebook_name():
    from IPython.core.display import Javascript
    from IPython.display import display as idisplay
    """Returns the name of the current notebook as a string

    From From https://mail.scipy.org/pipermail/ipython-dev/2014-June/014096.html
    """
    idisplay(Javascript('IPython.notebook.kernel.execute("theNotebook = " + \
    "\'"+IPython.notebook.notebook_name+"\'");'))
    return theNotebook


def get_cur_file_name():
    if is_notebook():
        return get_notebook_name()
    else:
        return __file__


def get_cur_file_version():
    import re
    m = re.search(r"\d+_\d+_\d+", get_cur_file_name())
    if m is None:
        raise ValueError("Illegal python file name, missed version info such as X_X_X (X is number)")
    return m.group(0)


def get_ver_num(file_ver_num):
    a, b, c = file_ver_num.split("_")
    return 10000 * a + 100 * b + c


def check_file_ver(compare_file_ver):
    cur_file_ver = get_cur_file_version()
    return get_ver_num(cur_file_ver) > get_ver_num(compare_file_ver)


def transform_args_data(args_value, output_folder):
    if os.path.exists(args_value):
        return args_value

    if ":" not in args_value:
        raise ValueError(f"Illegal file path {args_value}")

    file_path = os.path.join(output_folder, args_value.split(":")[0])
    list_of_files = os.listdir(file_path)

    pre_file_ver, file_name = args_value.split(":")
    if not check_file_ver(pre_file_ver):
        raise ValueError(f"Current file version is larger than precedent {pre_file_ver}")

    if "." in file_name:
        file_base_name, file_extention = file_name.split(".")
    else:
        file_base_name, file_extention = file_name, None

    list_of_files = [os.path.join(file_path, basename) for basename in list_of_files
                     if basename.split(".")[0] in file_base_name]

    if file_extention:
        list_of_files = [x for x in list_of_files if x.split(".")[-1] in file_extention]

    if not len(list_of_files):
        raise ValueError(f"Cannot search {file_name} in default folder {file_path} is empty!")

    return max(list_of_files, key=os.path.getctime)


def get_args_data(args_value):
    if os.path.exists(args_value):
        return args_value

    # 对于 notebook 中，如果文件不存在，自动探索
    if is_notebook():
        root_path = os.path.join(os.path.abspath(os.curdir), default_relative_output_path)
        if ":" not in args_value:
            raise ValueError(f"Illegal file path {args_value}")
        file_path = os.path.join(root_path, *args_value.split(":"))

        # 对于后缀符合要求的文件，只返回最新的结果，最新以文件创建时间来判断
        valid_extensions = ["txt", "parquet", "csv", "xlsx", "xls"]
        list_of_files = os.listdir(file_path)
        list_of_files = [os.path.join(file_path, basename) for basename in list_of_files
                         if basename.split(".")[-1] in valid_extensions]
        if not len(list_of_files):
            raise ValueError(f"Default folder {file_path} is empty!")

        return max(list_of_files, key=os.path.getctime)

    raise ValueError(f"Cannot find {args_value}")


def get_output_folder(args_value):
    # 如果不是 None，那必须是有价值的东西
    if args_value:
        if os.path.exists(args_value):
            return os.path.abspath(args_value)
        else:
            raise ValueError(f"Cannot find path {args_value}")

    # 对于 notebook 中，根据自身的编号创建对应的文件夹
    if is_notebook():
        root_path = os.path.join(os.path.abspath(os.curdir), default_relative_output_path)
        output_folder = os.path.join(root_path, get_cur_file_version())
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        return output_folder

    raise ValueError(f"Cannot find {args_value}")

