from .hunterdouglasplatinum import HunterDouglasPlatinumHub
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip",
                        help="ip address of the hub")
    parser.add_argument("-d", "--shade",
                        help="name of the shade (optional)")
    parser.add_argument("-n", "--scene",
                        help="name of the scene (optional)")
    parser.add_argument("-l", "--level",
                        help="level of the shade (optional) - can be up/down/percentage")
    args = parser.parse_args()

    if args.ip:
        hub = HunterDouglasPlatinumHub(args.ip)
        if(args.shade):
            shade = hub.get_shade(args.shade)
            if shade:
                if args.level:
                    shade.set_level(args.level)
                else:
                    print('need to specify level using --level')
            else:
                print('Shade not found')
    else:
        print('IP address of hub not specified')

if __name__ == "__main__":
    main()
