
class LogManager(object):
    @classmethod
    def write_log(cls, content, log_file_name):
        file_name = log_file_name
        with open(file_name, 'a+') as f:
            f.write(content.encode("utf-8").decode("utf-8"))

