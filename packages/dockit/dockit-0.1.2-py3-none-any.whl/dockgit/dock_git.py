"""
Ron's lazy CLI set
"""
import argparse
import os
import subprocess


class ColorTag:
    RESET = '\x1b[0m'

    RED = '\x1b[5;31;40m'
    BLUE = '\x1b[5;34;40m'
    YELLOW = '\x1b[5;33;40m'

    ON_RED = '\x1b[5;30;41m'
    ON_BLUE = '\x1b[5;30;44m'
    ON_YELLOW = '\x1b[5;30;43m'

    RED_ON_YELLOW = '\x1b[5;31;43m'
    BLUE_ON_YELLOW = '\x1b[3;34;43m'
    YELLOW_ON_RED = '\x1b[5;33;41m'
    YELLOW_ON_BLUE = '\x1b[5;33;44m'


class DockGit:

    _PROJECT_PATH = str()
    _PROJECT_NAME = str()
    _SERVICE_NAME = str()

    try:
        _TERMINAL_SIZE_WIDTH = os.get_terminal_size().columns
    except:
        _TERMINAL_SIZE_WIDTH = 90

    @classmethod
    def _get_args(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-n', '--project-name',
            help='appoint specific project name',
            type=str,
        )
        parser.add_argument(
            '-p', '--git-pull',
            action='store_true',
            help='pull git repository and all sub repositories',
        )
        parser.add_argument(
            '-l', '--docker-launch-service',
            action='store_true',
            help='launch service in the same prefix project',
        )
        parser.add_argument(
            '-c', '--docker-close-service',
            action='store_true',
            help='close service in the same prefix project',
        )
        parser.add_argument(
            '-r', '--docker-exec-container',
            action='store_true',
            help='exec docker container',
        )
        parser.add_argument(
            '-s', '--docker-show-containers',
            action='store_true',
            help='show docker processes',
        )
        return parser.parse_args()

    @staticmethod
    def _get_project_path():
        return subprocess.getoutput('git rev-parse --show-toplevel')

    @classmethod
    def _get_project_name(cls):
        return os.path.basename(cls._PROJECT_PATH) if cls._PROJECT_PATH else None

    @classmethod
    def _get_service_name(cls):
        if not cls._PROJECT_NAME:
            return None
        prefix = cls._PROJECT_NAME.split('_', 1)[0]
        return f'{prefix}_service'

    @classmethod
    def _git_pull(cls):
        os.system('git pull')
        os.system(
            f"grep path '{cls._PROJECT_PATH}/.gitmodules' | "
            f"sed 's/.*= //' | "
            f"xargs -I@ git -C {cls._PROJECT_PATH}/@ pull"
        )

    @classmethod
    def _show_launch_service_info(cls, service):
        print (
            f'{ColorTag.BLUE} {ColorTag.ON_BLUE} UP {ColorTag.YELLOW_ON_BLUE} {ColorTag.RESET}'
            f'{ColorTag.ON_YELLOW} {service} {ColorTag.YELLOW}{ColorTag.RESET}'
        )

    @classmethod
    def _launch_docker_service(cls):
        service = cls._SERVICE_NAME
        if not service:
            raise Exception('service name not found')
        pathname = os.path.expanduser(f'~/{service}/docker-compose.yml')
        cls._show_launch_service_info(service=service)
        os.system(f'docker-compose -f "{pathname}" up -d')

    @classmethod
    def _show_close_service_info(cls, service):
        print (
            f'{ColorTag.YELLOW}{ColorTag.ON_YELLOW} {service} {ColorTag.YELLOW_ON_RED} {ColorTag.RESET}'
            f'{ColorTag.ON_RED} DOWN {ColorTag.RED}  {ColorTag.RESET}'
        )

    @classmethod
    def _close_docker_service(cls):
        service= cls._SERVICE_NAME
        if not service:
            raise Exception('service name not found')
        pathname = os.path.expanduser(f'~/{service}/docker-compose.yml')
        cls._show_close_service_info(service=service)
        os.system(f'docker-compose -f "{pathname}" down')

    @classmethod
    def _show_exec_info(cls, container):
        os.system('clear')
        print (
            f'{"  CONTAINER ":^{cls._TERMINAL_SIZE_WIDTH}}\n'
            f'{ColorTag.BLUE} {ColorTag.ON_BLUE} RUN {ColorTag.BLUE_ON_YELLOW} {ColorTag.RESET}'
            f'{ColorTag.ON_YELLOW}   {container} {ColorTag.YELLOW}  {ColorTag.RESET}'
        )

    @classmethod
    def _exec_container(cls):
        container = cls._PROJECT_NAME
        if not container:
            raise Exception('cannot parse project name')
        if not subprocess.getoutput(f'docker ps -q -f name={container}'):
            raise Exception('container not found')
        cls._show_exec_info(container=container)
        os.system(f'docker exec -it {container} bash -l')

    @classmethod
    def _show_containers(cls):
        os.system(r'docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}\t{{.Image}}"')

    @classmethod
    def cli(cls):
        args = cls._get_args()
        cls._PROJECT_PATH = cls._get_project_path()
        cls._PROJECT_NAME = args.project_name or cls._get_project_name()
        cls._SERVICE_NAME = cls._get_service_name()
        if args.git_pull:
            cls._git_pull()
        if args.docker_launch_service:
            cls._launch_docker_service()
        if args.docker_close_service:
            cls._close_docker_service()
        if args.docker_exec_container:
            cls._exec_container()
        if args.docker_show_containers:
            cls._show_containers()

if __name__ == '__main__':
    DockGit.cli()

