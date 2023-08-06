#!/usr/bin/python3

# imports

from .__init__ import __doc__ as description, __version__ as version
from argparse import ArgumentParser as Parser, RawDescriptionHelpFormatter as Formatter
from os import getenv, popen, environ
from os.path import abspath, join as joinpath, split as splitpath, expanduser, isfile
from sys import argv, exit
from warnings import simplefilter

# classes

class args:
    "container for arguments"
    pass

# constants

path_wmtile = environ['HOME'] + "/.local/bin/wmtile"

comment = {"m": "Minimize all windows in current workspace",
    "t": "reshape as Tiles all windows in current workspace",
    "p": "reshape as Portraits all windows in current workspace",
    "l": "reshape as Landscapes all windows in current workspace",
    "s": "reshape as a Stack all windows in current workspace",
    "b": "reshape as Big (maximize) all windows in current workspace",
    "c": "gracefully Close all windows in current workspace"}

# generic functions

def file(name):
    "get absolute path of file in package"
    return joinpath(splitpath(__file__)[0], name)

def shell(command):
    "perform shell command and return stdout as a list of notempty rstripped lines"
    return [line for line in [line.rstrip() for line in popen(command)] if line]

# specific functions

def reshape(window, xpos, ypos, width, height):
    "reshape a window"
    shell(f"wmctrl -i -a {window}")
    shell(f"wmctrl -i -r {window} -b remove,maximized_vert,maximized_horz")
    shell(f"wmctrl -i -r {window} -e 0,{xpos},{ypos},{width},{height}")
    
# main functions

def wmtile(argv): 
    "window tiler for XFCE and many other desktop environments"

    # check external programs
    wmctrl = bool(shell("which wmctrl"))
    xdotool = bool(shell("which xdotool"))
    if not wmctrl and not xdotool:
        exit("wmctrl and xdotool not found, please install, eg:\n\n    $ sudo apt-get -y install wmctrl and not xdotool")
    elif not wmctrl:
        exit("wmctrl not found, please install, eg:\n\n    $ sudo apt-get -y install wmctrl")
    elif not xdotool:
        exit("xdotool not found, please install, eg:\n\n    $ sudo apt-get -y install xdotool")

    # get arguments
    parser = Parser(prog="wmtile", formatter_class=Formatter, description=description)
    parser.add_argument('-H', '--user-guide', action='store_true', help="open User Guide in PDF format and exit")
    parser.add_argument("-V", "--version",    action="version",    version="wmtile " + version)
    parser.add_argument("-i", "--launchers",  action="store_true", help="install 7 panel launchers (XFCE only)")
    parser.add_argument("-k", "--shortcuts",  action="store_true", help="install 7 keyboard shortcuts (XFCE only)")
    parser.add_argument("-m", "--minimize",   action="store_true", help=comment["m"])
    parser.add_argument("-t", "--tiles",      action="store_true", help=comment["t"])
    parser.add_argument("-p", "--portraits",  action="store_true", help=comment["p"])
    parser.add_argument("-l", "--landscapes", action="store_true", help=comment["l"])
    parser.add_argument("-s", "--stack",      action="store_true", help=comment["s"])
    parser.add_argument("-b", "--big",        action="store_true", help=comment["b"])
    parser.add_argument("-c", "--close",      action="store_true", help=comment["c"])
    parser.parse_args(argv[1:], args)

    # check arguments
    n_options = (args.user_guide + args.launchers + args.shortcuts + args.minimize + args.tiles +
                 args.portraits + args.landscapes + args.stack + args.big + args.close)
    if n_options != 1:
        exit(f"options are {n_options} but they must be exactly 1")
    if args.user_guide:
        shell(f"xdg-open {file('docs/wmtile.pdf')} &")
        exit()

    # get parameters
    parameters = {
        "top_margin":   32,
        "bottom_margin": 0,
        "left_margin":   0,
        "right_margin":  0,
        "bottom_space": 36,
        "right_space":  12,
        "top_stack":    20,
        "left_stack":   20}
    cfg = expanduser("~/.config/wmtile/parameters.cfg")
    if isfile(cfg):
        for jline, line in enumerate(open(cfg)):
            line = line.lower().split("#")[0].strip()
            if line:
                try:
                    name, value = line.split("=")
                    name = name.strip()
                    assert name in parameters
                    value = int(value)
                    assert value >= 0
                    parameters[name] = value
                except:
                    exit(f"error in line {jline+1} {line!r} of file {cfg!r}")
    top_margin    = parameters["top_margin"]
    bottom_margin = parameters["bottom_margin"]
    left_margin   = parameters["left_margin"]
    right_margin  = parameters["right_margin"]
    bottom_space  = parameters["bottom_space"]
    right_space   = parameters["right_space"]
    top_stack     = parameters["top_stack"]
    left_stack    = parameters["left_stack"]
    
    # perform
    if args.launchers: # wmtile -i
        if not shell("which xfce4-panel"):
            exit("error: XFCE4 not found")
        print("installing 7 wmtile keyboard shortcuts")
        for x in "mtplsbc":
            desktop = file(f"desktops/wmtile-{x}.desktop")
            icon = file(f"icons/wmtile-{x}.ico")
            open(desktop, "w").write(f"""[Desktop Entry]
Name=wmtile -{x}
Exec={path_wmtile} -{x}
Comment={comment[x]}
Icon={icon}
Terminal=false
Type=Application
StartupNotify=false
MimeType=text/plain;
Categories=Utility;""")
            shell(f"xfce4-panel --add=launcher {desktop}")
            print(f"    panel launcher --> wmtile -{x} ({comment[x]})")
    elif args.shortcuts: # wmtile -k
        xml = expanduser("~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml")
        if not isfile(xml):
            exit("error: XFCE4 not found")
        buf = [line.rstrip() for line in open(xml)]
        first = True
        print("installing 7 wmtile keyboard shortcuts")
        with open(xml, "w") as out:
            for line in buf:
                if "wmtile" not in line:
                    print(line, file=out)
                if first and '<property name="custom" type="empty">' in line:
                    first = False
                    for x in "mtplsbc":
                        X = x.upper()
                        print(f'    <property name="&lt;Alt&gt;&lt;Shift&gt;{X}" type="string" value="{path_wmtile} -{x}"/>', file=out)
                        print(f"    Alt+Shift+{X} --> wmtile -{x} ({comment[x]})")
        print("please reboot in order to make wmtile keyboard shortcuts effective")
    else:
        desktop = [d for d in shell("wmctrl -d") if "*" in d][0]
        fields = desktop.replace("x"," ").replace(","," ").split()
        j_desktop, screen_width, screen_height = [int(fields[j]) for j in [0, 3, 4]]
        area_xpos = left_margin
        area_ypos = top_margin
        area_width = screen_width - left_margin - right_margin
        area_height = screen_height - top_margin - bottom_margin
        windows = [w[0] for w in [w.split() for w in shell("wmctrl -l")] if int(w[1]) == j_desktop]
        n_windows = len(windows)
        if windows:
            if args.minimize: # wmtile -m
                for window in windows: 
                    shell(f"xdotool windowminimize {window}") # impossible by wmctrl
            elif args.stack: # wmtile -s
                window_width = area_width - left_stack * (n_windows - 1) - right_space
                window_height = area_height - top_stack * (n_windows - 1) - bottom_space
                for window_index, window in enumerate(windows):
                    window_xpos = area_xpos + left_stack * window_index
                    window_ypos = area_ypos + top_stack * window_index
                    reshape(window, window_xpos, window_ypos, window_width, window_height)
            elif args.big: # wmtile -b
                window_xpos, window_ypos = left_margin, top_margin
                window_width, window_height = area_width - right_space, area_height - bottom_space
                for window in windows: 
                    reshape(window, window_xpos, window_ypos, window_width, window_height)
            elif args.close: # wmtile -c
                for window in windows:
                    shell(f"wmctrl -i -c {window}")
            else:
                if args.tiles: # wmtile -t 
                    for n_rows, n_cols in ((r, c) for c in range(1, 100) for r in [c, c + 1]):
                        if n_rows * n_cols >= n_windows:
                            break
                elif args.landscapes: # wmtile -l
                    n_rows, n_cols = 1, n_windows 
                else: # wmtile -p
                    n_rows, n_cols = n_windows, 1 
                window_width = area_width // n_rows - right_space
                window_height = area_height // n_cols - bottom_space
                for window_index, window in enumerate(windows):
                    j_row, j_col = divmod(window_index, n_rows)
                    window_xpos = area_xpos + j_col * (window_width + right_space)
                    window_ypos = area_ypos + j_row * (window_height + bottom_space)
                    reshape(window, window_xpos, window_ypos, window_width, window_height)
                        
def main():
    try:
        simplefilter("ignore")
        wmtile(argv)
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
