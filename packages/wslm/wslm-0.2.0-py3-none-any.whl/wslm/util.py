def get_fire_wall_rule_args(wall):
    if not isinstance(wall, list):
        return None
    return list(set(wall))


class Color:
    """
    控制台字体颜色更改
    """

    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BlUE = '\033[94m'
    END = '\033[0m'

    @classmethod
    def red(cls, string):
        return cls.RED + str(string) + cls.END

    @classmethod
    def green(cls, string):
        return cls.GREEN + str(string) + cls.END

    @classmethod
    def yellow(cls, string):
        return cls.YELLOW + str(string) + cls.END

    @classmethod
    def cyan(cls, string):
        return cls.BlUE + str(string) + cls.END
