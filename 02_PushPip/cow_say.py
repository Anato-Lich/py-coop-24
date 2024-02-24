import argparse
import cowsay

def parse_arguments():
    parser = argparse.ArgumentParser(description='Python implementation of cowsay')
    parser.add_argument('message', nargs='?', default='Hello, World!', help='The message to be displayed by the cow')
    
    # cow type
    parser.add_argument('-b', '--borg', action='store_true', help='Use the Borg cow')
    parser.add_argument('-d', '--dead', action='store_true', help='Use the Dead cow')
    parser.add_argument('-g', '--greedy', action='store_true', help='Use the Greedy cow')
    parser.add_argument('-p', '--paranoid', action='store_true', help='Use the Paranoid cow')
    parser.add_argument('-s', '--stoned', action='store_true', help='Use the Stoned cow')
    parser.add_argument('-t', '--tired', action='store_true', help='Use the Tired cow')
    parser.add_argument('-w', '--wired', action='store_true', help='Use the Wired cow')
    parser.add_argument('-y', '--youthful', action='store_true', help='Use the Youthful cow')
    
    # eye, cow_file, list
    parser.add_argument('-e', '--eye', help='Specify the cow\'s eye')
    parser.add_argument('-f', '--file', help='Specify a cowfile')
    parser.add_argument('-l', '--list', action='store_true', help='Call cowsay.list_cows()')
    
    # tongue and wrap
    parser.add_argument('-T', '--tongue', help='Specify the cow\'s tongue')
    parser.add_argument('-W', '--wrap', type=int, help='Specify maximum column width for output')
    
    # no-wrap
    parser.add_argument('-n', '--no-wrap', action='store_true', help='Do not use word-wrapping')
    
    return parser.parse_args()

def main():
    args = parse_arguments()
    # print(args)

    if args.list:
        print(cowsay.list_cows())
    else:
        cow = 'default'
        if args.borg:
            cow = 'borg'
        elif args.dead:
            cow = 'dead'
        elif args.greedy:
            cow = 'greedy'
        elif args.paranoid:
            cow = 'paranoid'
        elif args.stoned:
            cow = 'stoned'
        elif args.tired:
            cow = 'tired'
        elif args.wired:
            cow = 'wired'
        elif args.youthful:
            cow = 'youthful'

        eye = args.eye if args.eye else 'oo'
        file = args.file if args.file else None
        
        tongue = args.tongue if args.tongue else '  '
        wrap = args.wrap if args.wrap else 40
        
        no_wrap = False if args.no_wrap else True
        
        print(cowsay.cowsay(message=args.message, cowfile=file, cow=cow, eyes=eye, wrap_text=no_wrap, tongue=tongue, width=wrap))

if __name__ == '__main__':
    main()
