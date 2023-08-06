import argparse


def tma():
    print('call tma')


def tmb():
    parser = argparse.ArgumentParser()
    parser.add_argument("-name", default="Default name")
    args = parser.parse_args()
    print('The name is %s' % args.name)
