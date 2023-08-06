import re
import subprocess


class WindowsCommandBase:
    """
    命令基类
    """

    POWER_SHELL = 'PowerShell.exe'

    IPV4_PATTERN = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

    @classmethod
    def get_wsl_ip(cls):
        """
        获取WSL2的IP
        :return:
        """

        wsl_cmd = "ifconfig eth0 | grep 'inet '"

        _result = cls.run_cmd(cmd=wsl_cmd)
        wsl_ip = re.search(cls.IPV4_PATTERN, _result).group(0)
        return wsl_ip

    @classmethod
    def run_cmd(cls, cmd: str, encoding='gbk'):
        _result = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            bufsize=-1,
            encoding=encoding
        )
        _result.wait()
        data = _result.stdout.read()
        return data


class WindowsCommandPort(WindowsCommandBase):
    """
    端口转发
    """

    CMD_PORT_PRE = '{power_shell} netsh interface portprox'

    CMD_PORT_ADD = '{pre} add v4tov4 listenport={port} listenaddress={addr} connectport={port} connectaddress={ip}'

    CMD_PORT_DEL = '{pre} delete v4tov4 listenport={port} listenaddress={addr}'

    CMD_PORT_INFO = '{pre} show all'

    CMD_PORT_RESET = '{pre} reset'

    def info(self, power_shell: str = WindowsCommandBase.POWER_SHELL):
        cmd = self.CMD_PORT_INFO.format(pre=self.__get_cmd_port_pre(power_shell=power_shell))
        result_string = self.run_cmd(cmd).splitlines()
        _result = []
        for key, line in enumerate(result_string):
            if key < 5:
                continue
            line = line.strip().split()
            if len(line) == 4:
                _result.append({
                    'listen_address': line[0],
                    'listen_port': int(line[1]),
                    'connect_address': line[2],
                    'connect_port': int(line[3]),
                })
        return _result

    def add(self, port: int, addr: str = '0.0.0.0', ip: str = '', power_shell: str = WindowsCommandBase.POWER_SHELL):
        """
        添加端口
        :param port:
        :param addr:
        :param ip:
        :param power_shell:
        :return:
        """

        cmd = self.__get_cmd_port_add(port=port, addr=addr, ip=ip, power_shell=power_shell)
        return self.run_cmd(cmd)

    def delete(self, port: int, addr: str = '0.0.0.0', power_shell: str = WindowsCommandBase.POWER_SHELL):
        """
        删除端口
        :param port:
        :param addr:
        :param power_shell:
        :return:
        """

        cmd = self.__get_cmd_port_del(port=port, addr=addr, power_shell=power_shell)
        return self.run_cmd(cmd)

    def reset(self, power_shell: str = WindowsCommandBase.POWER_SHELL):
        """
        清除所有的端口转发
        :param power_shell:
        :return:
        """

        cmd = self.CMD_PORT_RESET.format(pre=self.__get_cmd_port_pre(power_shell=power_shell))
        return self.run_cmd(cmd)

    def __get_cmd_port_pre(self, power_shell: str) -> str:
        cmd = self.CMD_PORT_PRE.format(
            power_shell=power_shell
        )
        return cmd

    def __get_cmd_port_add(self, port: int, addr: str, ip: str, power_shell: str) -> str:
        """
        获取添加端口转发的命令字符串
        :param port: 要转发的端口
        :param addr: 监听地址
        :param ip: 监听IP，为空时自动获取wsl的ip
        :param power_shell: PowerShell.exe 路径
        :return:
        """

        cmd = self.CMD_PORT_ADD.format(
            pre=self.__get_cmd_port_pre(power_shell=power_shell),
            port=port,
            addr=addr,
            ip=ip if ip else self.get_wsl_ip()
        )
        return cmd

    def __get_cmd_port_del(self, port: int, addr: str, power_shell: str) -> str:
        """
        获取删除端口转发的命令字符串
        :param port: 要转发的端口
        :param addr: 监听地址
        :param power_shell: PowerShell.exe 路径
        :return:
        """

        cmd = self.CMD_PORT_DEL.format(
            pre=self.__get_cmd_port_pre(power_shell=power_shell),
            port=port,
            addr=addr,
        )
        return cmd


class WindowsCommandFireWall(WindowsCommandBase):
    """
    防火墙管理
    """

    FIRE_WALL_RULE_OUT = 'Outbound'

    FIRE_WALL_RULE_IN = 'Inbound'

    FIRE_WALL_RULE_ALL = 'ALL'

    WALL_TYPES = [
        FIRE_WALL_RULE_IN,
        FIRE_WALL_RULE_OUT
    ]

    WALL_NAME = 'WSL 2 Firewall Unlock'

    CMD_WALL_ADD = "{power_shell} \"New-NetFireWallRule -DisplayName '{wall_name}' -Direction '{wall_type}' -LocalPort {port} -Action Allow -Protocol TCP\""

    CMD_WALL_DEL = "{power_shell} \"Remove-NetFireWallRule -DisplayName '{wall_name}'\""

    def add_in(self, port: int, power_shell: str):
        """
        添加入方向防火墙
        :param port:
        :param power_shell:
        :return:
        """
        cmd = self.__get_cmd_wall_inbound_add(port=port, power_shell=power_shell)
        return self.run_cmd(cmd)

    def add_out(self, port: int, power_shell: str):
        """
        添加出方向防火墙
        :param port:
        :param power_shell:
        :return:
        """
        cmd = self.__get_cmd_wall_outbound_add(port=port, power_shell=power_shell)
        return self.run_cmd(cmd)

    def delete_in(self, port: int, power_shell: str):
        """
        删除入方向防火墙
        :param port:
        :param power_shell:
        :return:
        """
        cmd = self.__get_cmd_wall_inbound_del(port=port, power_shell=power_shell)
        return self.run_cmd(cmd)

    def delete_out(self, port: int, power_shell: str):
        """
        删除出方向防火墙
        :param port:
        :param power_shell:
        :return:
        """
        cmd = self.__get_cmd_wall_outbound_del(port=port, power_shell=power_shell)
        return self.run_cmd(cmd)

    def __get_cmd_wall_inbound_add(self, port: int, power_shell: str) -> str:
        """
        获取添加入方向防火墙命令字符串
        :param port:
        :param power_shell:
        :return:
        """
        return self.__get_cmd_wall_add(port=port, wall_type=self.FIRE_WALL_RULE_IN, power_shell=power_shell)

    def __get_cmd_wall_outbound_add(self, port: int, power_shell: str) -> str:
        """
        获取添加出方向防火墙命令字符串
        :param port:
        :param power_shell:
        :return:
        """
        return self.__get_cmd_wall_add(port=port, wall_type=self.FIRE_WALL_RULE_OUT, power_shell=power_shell)

    def __get_cmd_wall_add(self, port: int, wall_type: str, power_shell: str) -> str:
        """
        获取添加防火墙命令字符串
        :param port:
        :param wall_type:
        :param power_shell:
        :return:
        """

        cmd = self.CMD_WALL_ADD.format(
            wall_name='{name} {port} {type}'.format(name=self.WALL_NAME, port=port, type=wall_type),
            port=port,
            wall_type=wall_type,
            power_shell=power_shell,
        )
        return cmd

    def __get_cmd_wall_inbound_del(self, port: int, power_shell: str) -> str:
        """
        获取删除入方向防火墙命令字符串
        :param port:
        :param power_shell:
        :return:
        """

        return self.__get_cmd_wall_del(port=port, wall_type=self.FIRE_WALL_RULE_IN, power_shell=power_shell)

    def __get_cmd_wall_outbound_del(self, port: int, power_shell: str) -> str:
        """
        获取删除出方向防火墙命令字符串
        :param port:
        :param power_shell:
        :return:
        """

        return self.__get_cmd_wall_del(port=port, wall_type=self.FIRE_WALL_RULE_OUT, power_shell=power_shell)

    def __get_cmd_wall_del(self, port: int, wall_type: str, power_shell: str) -> str:
        """
        获取删除防火墙命令字符串
        :param port:
        :param wall_type:
        :param power_shell:
        :return:
        """

        cmd = self.CMD_WALL_DEL.format(
            wall_name='{name} {port} {type}'.format(name=self.WALL_NAME, port=port, type=wall_type),
            power_shell=power_shell,
        )

        return cmd
