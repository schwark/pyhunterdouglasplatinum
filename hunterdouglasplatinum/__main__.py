from .hunterdouglasplatinum import HunterDouglasPlatinumHub
import argparse
import sys

def err(msg):
    sys.stderr.write(msg+"\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip",
                        help="ip address of the hub")
    parser.add_argument("-d", "--shade",
                        help="name of the shade")
    parser.add_argument("-n", "--scene",
                        help="name of the scene")
    parser.add_argument("-l", "--level",
                        help="level of the shade <up/down/percentage>")
    args = parser.parse_args()

    if args.ip:
        hub = HunterDouglasPlatinumHub(args.ip)
        if(args.shade):
            shade = hub.get_shade(name=args.shade)
            if(shade):
                if args.level:
                    shade.set_level(args.level)
                else:
                    err("need to specify level using --level")
            else:
                err("Shade not found")
        elif(args.scene):
            scene = hub.get_scene(name=args.scene)
            if(scene):
                scene.run()
            else:
                err('Scene not found')
    else:
        err('IP address of hub not specified')

if __name__ == "__main__":
    main()
