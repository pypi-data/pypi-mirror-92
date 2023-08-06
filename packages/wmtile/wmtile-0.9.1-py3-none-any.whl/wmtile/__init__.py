"""window tiler for XFCE desktop environment

wmtile is a CLI program, but you should use it either by mouse (via wmtile -i)...

    $ wmtile -k
    installing 7 wmtile keyboard shortcuts
        Alt+Shift+M --> wmtile -m (Minimize all windows in current workspace)
        Alt+Shift+T --> wmtile -t (reshape as Tiles all windows in current workspace)
        Alt+Shift+P --> wmtile -p (reshape as Portraits all windows in current workspace)
        Alt+Shift+L --> wmtile -l (reshape as Landscapes all windows in current workspace)
        Alt+Shift+S --> wmtile -s (reshape as a Stack all windows in current workspace)
        Alt+Shift+B --> wmtile -b (reshape as Big (maximize) all windows in current workspace)
        Alt+Shift+C --> wmtile -c (gracefully Close all windows in current workspace)
    please reboot in order to make wmtile keyboard shortcuts effective

...or by keyboard (via wmtile -k)

    $ wmtile -i
    installing 7 wmtile panel launchers
        panel launcher --> wmtile -m (Minimize all windows in current workspace)
        panel launcher --> wmtile -t (reshape as Tiles all windows in current workspace)
        panel launcher --> wmtile -p (reshape as Portraits all windows in current workspace)
        panel launcher --> wmtile -l (reshape as Landscapes all windows in current workspace)
        panel launcher --> wmtile -s (reshape as a Stack all windows in current workspace)
        panel launcher --> wmtile -b (reshape as Big (maximize) all windows in current workspace)
        panel launcher --> wmtile -c (gracefully Close all windows in current workspace)

for further details, type:

    $ wmtile -H
"""

__version__ = "0.9.1"
