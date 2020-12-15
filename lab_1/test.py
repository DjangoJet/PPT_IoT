import argparse

my_parser = argparse.ArgumentParser()
my_parser.add_argument('-i', action='store', type=str, required=True)
my_parser.add_argument('-p', action='store', type=int, required=True)

args = my_parser.parse_args()

print('Ip arg type: {}, value: {}'.format(type(args.i), args.i))
print('Port arg type: {}, value: {}'.format(type(args.p), args.p))