import argparse

from .windows_command import WindowsCommandBase, WindowsCommandPort, WindowsCommandFireWall


class WindowsCommandArgParse:
    """
    命令解析类
    """

    def __init__(self):
        """
        初始化命令解析
        """

        self._parser = argparse.ArgumentParser(prog='wslm')
        self._subparsers = self._parser.add_subparsers(title='available commands')
        self._parser.add_argument(
            '-s',
            '--power_shell',
            default=WindowsCommandBase.POWER_SHELL,
            help='PowerShell.exe 可执行文件路径'
        )
        self._parser.set_defaults(func=lambda *args, **kwargs: self._parser.print_help())

    def _parser_cmd_port(self):
        # windows10 端口转发管理
        port = self._subparsers.add_parser(
            name='port',
            help='connect and listen wsl ports'
        )
        port_subparsers = port.add_subparsers(
            help='connect and listen wsl ports'
        )

        port.set_defaults(func=lambda *args, **kwargs: port.print_help())

        # # 添加端口转发
        port_add = port_subparsers.add_parser('add', help='add ports')
        port_add.add_argument(
            '-p',
            '--port',
            type=int,
            nargs='*',
            help='ports',
            required=True
        )
        port_add.add_argument(
            '-w',
            '--wall',
            type=str,
            nargs='*',
            default=WindowsCommandFireWall.FIRE_WALL_RULE_ALL,
            choices=WindowsCommandFireWall.WALL_TYPES,
            help='with firewall'
        )
        port_add.set_defaults(func=self.port_add_callback)

        # # 删除端口转发
        port_del = port_subparsers.add_parser('del', help='delete ports')
        port_del.add_argument(
            '-p',
            '--port',
            type=int,
            nargs='*',
            help='ports',
            required=True
        )
        port_del.add_argument(
            '-w',
            '--wall',
            type=str,
            nargs='*',
            default=WindowsCommandFireWall.FIRE_WALL_RULE_ALL,
            choices=WindowsCommandFireWall.WALL_TYPES,
            help='with firewall'
        )
        port_del.set_defaults(func=self.port_del_callback)

    def port_add_callback(self, namespace, parser, *args, **kwargs):
        """
        添加端口回调
        :param namespace:
        :param parser:
        :param args:
        :param kwargs:
        :return:
        """

        windows_command_port = WindowsCommandPort()
        windows_command_fire_wall = WindowsCommandFireWall()
        namespace.wall = self.get_fire_wall_rule_args(namespace.wall)
        namespace.port = list(set(namespace.port))
        for port in namespace.port:
            windows_command_port.add(port=port, power_shell=namespace.power_shell)
            if namespace.wall is None:
                continue
            for wall in namespace.wall:
                if wall == windows_command_fire_wall.FIRE_WALL_RULE_OUT:
                    windows_command_fire_wall.add_out(port=port, power_shell=namespace.power_shell)
                elif wall == windows_command_fire_wall.FIRE_WALL_RULE_IN:
                    windows_command_fire_wall.add_in(port=port, power_shell=namespace.power_shell)
            else:
                windows_command_fire_wall.add_out(port=port, power_shell=namespace.power_shell)
                windows_command_fire_wall.add_in(port=port, power_shell=namespace.power_shell)

    def port_del_callback(self, namespace, parser, *args, **kwargs):
        """
        删除端口回调
        :param namespace:
        :param parser:
        :param args:
        :param kwargs:
        :return:
        """

        windows_command_port = WindowsCommandPort()
        windows_command_fire_wall = WindowsCommandFireWall()
        namespace.wall = self.get_fire_wall_rule_args(namespace.wall)
        namespace.port = list(set(namespace.port))
        for port in namespace.port:
            windows_command_port.delete(port=port, power_shell=namespace.power_shell)
            if namespace.wall is None:
                continue
            for wall in namespace.wall:
                if wall == windows_command_fire_wall.FIRE_WALL_RULE_OUT:
                    windows_command_fire_wall.delete_out(port=port, power_shell=namespace.power_shell)
                elif wall == windows_command_fire_wall.FIRE_WALL_RULE_IN:
                    windows_command_fire_wall.delete_in(port=port, power_shell=namespace.power_shell)
            else:
                windows_command_fire_wall.delete_out(port=port, power_shell=namespace.power_shell)
                windows_command_fire_wall.delete_in(port=port, power_shell=namespace.power_shell)

    @staticmethod
    def get_fire_wall_rule_args(wall):
        if not isinstance(wall, list):
            return None
        return list(set(wall))

    def run(self):
        self._parser_cmd_port()
        # 解析参数，并执行回调方法
        _args = self._parser.parse_args()
        _func = getattr(_args, 'func', None)
        if _func:
            _func(namespace=_args, parser=self._parser)
        else:
            self._parser.print_help()


def main():
    """
    主方法
    :return:
    """

    windows_command_arg_parse = WindowsCommandArgParse()
    windows_command_arg_parse.run()


if __name__ == '__main__':
    main()
