"""xtapi script."""
import argparse


def do_init():
    data = """
from xtapi import MainApp

app = MainApp()

if __name__ == '__main__':
    app.run(name='main:app', reload=True, port=3900)
    """
    with open('main.py', 'w') as fd:
        fd.write(data.strip() + '\n')


def main():
    parser = argparse.ArgumentParser(description='xtapi helper')

    parser.add_argument('cmd', metavar='N', type=str,
                        help='请输入命令')

    args = parser.parse_args()

    cmd = args.cmd
    if cmd == 'init':
        do_init()
    else:
        print('不支持的命令')


if __name__ == '__main__':
    main()
