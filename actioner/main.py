from multiprocessing import Process

from aiohttp.web import run_app as run_web_app

from actioner.web import get_server


def main():
    server = get_server()
    web_process = Process(target=run_web_app, args=(server,))
    web_process.start()


if __name__ == '__main__':
    main()
