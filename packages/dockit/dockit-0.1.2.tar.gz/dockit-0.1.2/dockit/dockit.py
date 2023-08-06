"""
Ron's lazy CLI set
"""
import argparse
import os
import subprocess
import sys


class ColorTag:
    RESET = '\x1b[0m'

    RED = '\x1b[5;31;40m'
    BLUE = '\x1b[5;34;40m'
    CYAN = '\x1b[5;36;40m'
    GRAY = '\x1b[5;37;40m'
    GREEN = '\x1b[5;32;40m'
    YELLOW = '\x1b[5;33;40m'

    ON_RED = '\x1b[5;30;41m'
    ON_BLUE = '\x1b[5;30;44m'
    ON_CYAN = '\x1b[5;30;46m'
    ON_GRAY = '\x1b[5;30;47m'
    ON_GREEN = '\x1b[5;30;42m'
    ON_YELLOW = '\x1b[5;30;43m'

    RED_ON_YELLOW = '\x1b[5;31;43m'
    BLUE_ON_YELLOW = '\x1b[3;34;43m'
    GRAY_ON_CYAN = '\x1b[3;37;46m'
    GRAY_ON_RED = '\x1b[3;37;41m'
    YELLOW_ON_RED = '\x1b[5;33;41m'
    YELLOW_ON_BLUE = '\x1b[5;33;44m'


class Dockit:
    """
    Fuzzy the current location or appoint specific project name to
        - git
            + pull repository and all submodules

        - docker
            + launch the same prefix service with current project
            + close the same prefix service with current project
            + execute the container with the same as project

    usage: dockit.py [-h] [-n PROJECT_NAME] [-p] [-s] [-l] [-u] [-e] [-d] [-c]

    optional arguments:
      -h, --help            show this help message and exit
      -p, --git-pull        pull git repository and all sub repositories
      -n PROJECT_NAME, --project-name PROJECT_NAME
                            appoint specific project name
      -a, --docker-attach-container
                            to keep attaching mode after docker-compose upped
      -l, --docker-launch-service
                            parse project prefix and launch ${PREFIX}_service
      -c, --docker-close-service
                            parse project prefix and close ${PREFIX}_service
      -u, --docker-up-container
                            docker-compose up -d container with the same name as project
      -d, --docker-down-container
                            docker-compose down container with the same name as project
      -e, --docker-exec-container
                            docker exec -it container bash
      -s, --docker-show-containers
                            show docker processes
    """

    _PROJECT_PATH = str()
    _PROJECT_NAME = str()
    _SERVICE_NAME = str()

    try:
        _TERMINAL_SIZE_WIDTH = os.get_terminal_size().columns
    except:
        _TERMINAL_SIZE_WIDTH = 90

    @classmethod
    def _help(cls):
        print(cls.__doc__)
        sys.exit()

    @classmethod
    def _get_args(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '-n', '--project-name',
            help='appoint specific project name',
            type=str,
        )
        parser.add_argument(
            '-a', '--docker-attach-container',
            action='store_true',
            help='to keep attaching mode after docker-compose upped',
        )
        parser.add_argument(
            '-p', '--git-pull',
            action='store_true',
            help='pull git repository and all sub repositories',
        )
        parser.add_argument(
            '-l', '--docker-launch-service',
            action='store_true',
            help='parse project prefix and launch ${PREFIX}_service',
        )
        parser.add_argument(
            '-c', '--docker-close-service',
            action='store_true',
            help='parse project prefix and close ${PREFIX}_service',
        )
        parser.add_argument(
            '-u', '--docker-up-container',
            action='store_true',
            help='docker-compose up -d container with the same name as project',
        )
        parser.add_argument(
            '-d', '--docker-down-container',
            action='store_true',
            help='docker-compose down container with the same name as project',
        )
        parser.add_argument(
            '-e', '--docker-exec-container',
            action='store_true',
            help='docker exec -it container bash',
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
    def _get_submodules(cls):
        stdout = subprocess.getoutput(f'grep path \'{cls._PROJECT_PATH}/.gitmodules\' | sed \'s/.*= //\'')
        return {f'{cls._PROJECT_PATH}/{submodule}' for submodule in stdout.split('\n')}

    @staticmethod
    def _pull_command(path):
        repo = path.split('/')[-1]
        info = subprocess.getoutput(f'git -C {path} pull')
        if '已經是最新的' in info or 'Already up to date.' in info:
            return f'{ColorTag.YELLOW} {repo:<30} {ColorTag.GREEN}✔︎ {ColorTag.ON_GRAY}  {info}  {ColorTag.RESET}'
        return f'{ColorTag.YELLOW} {repo} {ColorTag.RESET}\n{info}'

    @classmethod
    def _git_pull(cls):
        """
        grep path '{cls._PROJECT_PATH}/.gitmodules' | sed 's/.*= //' | xargs -I@ git -C {cls._PROJECT_PATH}/@ pull
        """
        info = cls._pull_command(path=cls._PROJECT_PATH)
        print(f'{ColorTag.ON_BLUE} {"REPOSITORY":10}  {ColorTag.RESET} {info}')
        if not os.path.isfile(f'{cls._PROJECT_PATH}/.gitmodules'):
            sys.exit()
        for submodule in cls._get_submodules():
            info = cls._pull_command(path=submodule)
            print(f'{ColorTag.ON_CYAN}  {"SUBMODULE":10}  {ColorTag.RESET} {info}')

    @classmethod
    def _show_launch_service_info(cls, service):
        print (
            f'{ColorTag.BLUE} {ColorTag.ON_BLUE} LAUNCH {ColorTag.YELLOW_ON_BLUE} {ColorTag.RESET}'
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
            f'{ColorTag.ON_RED} CLOSE {ColorTag.RED}  {ColorTag.RESET}'
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
            f'{ColorTag.BLUE} {ColorTag.ON_BLUE} EXEC {ColorTag.BLUE_ON_YELLOW} {ColorTag.RESET}'
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
    def _show_up_info(cls, container):
        print (
            f'{ColorTag.GRAY}{ColorTag.ON_GRAY}   {container} {ColorTag.GRAY_ON_CYAN}  {ColorTag.RESET}'
            f'{ColorTag.ON_CYAN}{"UP":^10}{ColorTag.CYAN} {ColorTag.RESET}'
        )

    @classmethod
    def _up_container(cls, args):
        if not cls._PROJECT_NAME:
            raise Exception('cannot parse project name')
        cls._show_up_info(container=cls._PROJECT_NAME)
        if args.project_name:
            pathname = os.path.expanduser(f'~/{cls._PROJECT_NAME}/docker-compose.yml')
            command = f'docker-compose -f "{pathname}" up'
        else:
            command = f'docker-compose up'
        if args.docker_attach_container:
            os.system(command)
        os.system(f'{command} -d')

    @classmethod
    def _show_down_info(cls, container):
        print (
            f'{ColorTag.GRAY}{ColorTag.ON_GRAY}   {container} {ColorTag.GRAY_ON_RED}  {ColorTag.RESET}'
            f'{ColorTag.ON_RED}{"DOWN":^10}{ColorTag.RED} {ColorTag.RESET}'
        )

    @classmethod
    def _down_container(cls, args):
        if not cls._PROJECT_NAME:
            raise Exception('cannot parse project name')
        cls._show_down_info(container=cls._PROJECT_NAME)
        if args.project_name:
            pathname = os.path.expanduser(f'~/{cls._PROJECT_NAME}/docker-compose.yml')
            command = f'docker-compose -f "{pathname}" down'
        else:
            command = f'docker-compose down'
        os.system(command)

    @classmethod
    def _show_containers(cls):
        os.system(r'docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}\t{{.Image}}"')

    @classmethod
    def cli(cls):
        if len(sys.argv) == 1:
            cls._help()
        args = cls._get_args()
        cls._PROJECT_PATH = cls._get_project_path()
        cls._PROJECT_NAME = args.project_name or cls._get_project_name()
        cls._SERVICE_NAME = cls._get_service_name()

        """ GIT """
        if args.git_pull:
            cls._git_pull()

        """ CONTAINER """
        if args.docker_launch_service:
            cls._launch_docker_service()
        if args.docker_up_container:
            cls._up_container(args=args)
        if args.docker_exec_container:
            cls._exec_container()
        if args.docker_down_container:
            cls._down_container(args=args)
        if args.docker_close_service:
            cls._close_docker_service()
        if args.docker_show_containers:
            cls._show_containers()

