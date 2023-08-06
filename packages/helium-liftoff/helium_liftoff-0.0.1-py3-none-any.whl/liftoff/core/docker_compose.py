from liftoff.core.vars import LIFTOFF_PATH, LIFTOFF_APPS_PATH
from os import listdir
from os.path import isfile
from time import sleep, time
from .prompt import LiftoffPrompt
from subprocess import Popen, PIPE
from platform import system
from liftoff.builders.liftoff import LiftoffBuilder


TIMEOUT = 120


__LIFTOFF_PORTS = [
    80,    # NGINX
    1025,  # Mailhog
    3306,  # MySQL
    5432,  # PostgreSQL
    8025,  # Mailhog
    8079,  # Adminer
]


def start_liftoff():
    retry = False
    failed = False

    LiftoffBuilder.build()

    if not __start_liftoff_docker_compose():
        print('Failed to start liftoff services (possibly due to a port conflict).')
        response = LiftoffPrompt(text='Try killing Docker containers on conflicting ports?',
                                 options=['Y', 'n'],
                                 numbered=False,
                                 default='Y').prompt()

        if response == 'Y':
            retry = True
        else:
            failed = True

    if retry:
        retry = False

        if not __kill_conflicting_containers() or not __start_liftoff_docker_compose():
            print('Failed to start liftoff services (possibly due to a port conflict).')
            response = LiftoffPrompt(text='Try killing system processes on conflicting ports?',
                                     options=['Y', 'n'],
                                     numbered=False,
                                     default='Y').prompt()

            if response == 'Y':
                retry = True
            else:
                failed = True

    if retry:
        retry = False

        if not __kill_conflicting_processes() or not __start_liftoff_docker_compose():
            failed = True

    if failed:
        print('Failed to start liftoff services.')
        print('Please manually resolve the conflict, then try again.')
        print()
    else:
        print('Successfully started liftoff services.')


def __start_liftoff_docker_compose():
    host = system()

    success = False

    if host == 'Darwin':
        success = __start_docker_mac()
    elif host == 'Linux':
        success = __start_docker_linux()
    # elif host == 'Windows':
    #     # TODO
    #     pass
    else:
        print("Your system is not supported")
        exit(0)

    if not success:
        print("Failed to start Docker daemon.")
        print("Please start Docker on your system, then try again.")
        exit(0)

    command = f'docker-compose -f {LIFTOFF_PATH}/docker-compose.yml'

    for file in listdir(LIFTOFF_APPS_PATH):
        if isfile(f'{LIFTOFF_APPS_PATH}/{file}') and '.override.yml' in file:
            command = command + f' -f {LIFTOFF_APPS_PATH}/{file}'

    command = command + ' up -d'

    print('Staring liftoff services...')
    print()

    (output, err) = Popen(command, stdout=PIPE, stderr=PIPE, shell=True).communicate(timeout=TIMEOUT)

    if 'error' in str(output) or 'error' in str(err):
        return False

    sleep(5)

    return True


def __docker_is_running():
    status_command = 'docker stats --no-stream'
    process = Popen(status_command, stdout=PIPE, stderr=PIPE, shell=True)
    process.communicate()
    status = process.returncode

    return status == 0


def __start_docker_with_command(start_command: str):
    if not __docker_is_running():
        print('Starting Docker...')

        process = Popen(start_command, stdout=PIPE, stderr=PIPE, shell=True)
        process.communicate()
        status = process.returncode

        if status != 0:
            return False

        start_time = time()

        while not __docker_is_running():
            if time() - start_time > TIMEOUT:
                return False

        print('Successfully started Docker.')

    return True


def __start_docker_mac():
    return __start_docker_with_command('open --background -a Docker')


def __start_docker_linux():
    return __start_docker_with_command('sudo service docker start')


def __kill_conflicting_containers():
    subcommand = 'docker kill $(docker ps -q'
    for port in __LIFTOFF_PORTS:
        subcommand = subcommand + f' -f "publish={port}"'
    subcommand = subcommand + ')'

    (output, err) = Popen(subcommand, stdout=PIPE, stderr=PIPE, shell=True).communicate()

    if 'error' in str(output) or 'error' in str(err):
        return False

    return True


def __kill_conflicting_processes():
    for port in __LIFTOFF_PORTS:
        command = f'sudo kill -9 $(sudo lsof -t -i:{port})'
        (output, err) = Popen(command, stdout=PIPE, stderr=PIPE, shell=True).communicate()

        if 'error' in str(output) or 'error' in str(err):
            return False

    return True


def stop_liftoff():
    if __docker_is_running():
        retry = False
        failed = False

        print('Stopping liftoff services...')
        print()

        command = f'docker-compose -f {LIFTOFF_PATH}/docker-compose.yml stop'
        (output, err) = Popen(command, stdout=PIPE, stderr=PIPE, shell=True).communicate()

        if 'error' in str(output) or 'error' in str(err):
            print('Failed to stop liftoff services.')
            response = LiftoffPrompt(text='Try to force kill containers?',
                                     options=['Y', 'n'],
                                     numbered=False,
                                     default='Y').prompt()

            if response == 'Y':
                retry = True
            else:
                failed = True

        if retry:
            print('Killing liftoff services...')

            command = 'docker kill $(docker ps -q -f "name=liftoff")'
            (output, err) = Popen(command, stdout=PIPE, stderr=PIPE, shell=True).communicate()
            print()

            if 'error' in str(output) or 'error' in str(err):
                failed = True

        if failed:
            print("Failed to stop liftoff services.")
            print("Please manually stop all liftoff containers in Docker, then try again.")
            exit(0)
        else:
            print("Successfully stopped liftoff services.")
            print()

    else:
        print('Docker is not running.')


def restart_liftoff():
    print('Restarting Liftoff Services...')
    stop_liftoff()
    start_liftoff()
