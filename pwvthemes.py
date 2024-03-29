import sys

from PyQt6.QtGui import QColor
from PyQt6.QtGui import QPalette



def AffectiveTheme(wgt):
    pal = wgt.palette()
    cg = QPalette.ColorGroup.Current
    
    wc = pal.color(cg, QPalette.ColorRole.Window)
    wt = pal.color(cg, QPalette.ColorRole.WindowText)
    print(f"WC: {hex(wc.rgba())}  WT: {hex(wt.rgba())}")
# pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xffececec))
# pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xd8000000))

    if sys.platform == "darwin":
        if wc == QColor(0xff323232) and wt == QColor(0xd8ffffff):
            return "Dark"
        elif wc.rgba() == 0xffececec and wt.rgba() == 0xd8000000:
            return "Light"
    elif sys.platform[0:3] == "win":
        if wc.rgba() == 0xff323232 and wt.rgba() == 0xd8ffffff:
            return "Dark"
        elif wc.rgba() == 0xff1e1e1e and wt.rgba() == 0xffffffff:
            return "Dark"
        elif wc.rgba() == 0xfff0f0f0 and wt.rgba() == 0xff000000:
            return "Light"


def SetColorTheme(wgt, theme):
    theme = theme.lower()
    if sys.platform == "darwin":
        if theme == "dark":
            DarkPaletteApple(wgt)
            print("DarkPaletteApple")
        elif theme == "light":
            LightPaletteApple(wgt)
            print("LightPaletteApple")
    elif sys.platform[0:3] == "win":
        if theme == "dark":
            DarkPaletteWindows(wgt)
        elif theme == "light":
            LightPaletteWindows(wgt)
    elif sys.platform == "linux":
        if theme == "dark":
            DarkPaletteLinux(wgt)
        elif theme == "light":
            LightPaletteLinux(wgt)


def DarkPaletteApple(wgt):
    pal = wgt.palette()
    cg = QPalette.ColorGroup.Active
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xff989898))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xff171717))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xff314f78))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff3586ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xff242424))
    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xd8ffffff))

    cg = QPalette.ColorGroup.All
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xff989898))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xff171717))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xff314f78))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff3586ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xff242424))
#    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xd8ffffff))

    cg = QPalette.ColorGroup.Current
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xff989898))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xff171717))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xff314f78))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff3586ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xff242424))
#    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xd8ffffff))

    cg = QPalette.ColorGroup.Disabled
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xff989898))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xff363636))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff0000ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xff242424))
    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0x3fffffff))

    cg = QPalette.ColorGroup.Inactive
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xff989898))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xff171717))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xff363636))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff0000ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xff242424))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xd8ffffff))

def LightPaletteApple(wgt):
    pal = wgt.palette()
    cg = QPalette.ColorGroup.Active
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xfff5f5f5))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xffececec))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xd8000000))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xffa5cdff))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xd8000000))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff094fd1))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xffa9a9a9))
    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0x3f000000))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3f000000))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xd8000000))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xffececec))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xd8000000))

    cg = QPalette.ColorGroup.All
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xfff5f5f5))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xffececec))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xd8000000))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xffa5cdff))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xd8000000))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff094fd1))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xffa9a9a9))
#    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0x3f000000))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3f000000))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xd8000000))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xffececec))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xd8000000))

    cg = QPalette.ColorGroup.Current
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xfff5f5f5))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xffececec))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xd8000000))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xffa5cdff))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xd8000000))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff094fd1))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xffa9a9a9))
#    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0x3f000000))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3f000000))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xd8000000))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xffececec))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xd8000000))

    cg = QPalette.ColorGroup.Disabled
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xfff5f5f5))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xffececec))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xffececec))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0x3f000000))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xffd4d4d4))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0x3f000000))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff0000ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xffa9a9a9))
    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0xd8000000))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3f000000))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0x3f000000))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xffececec))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0x3f000000))

    cg = QPalette.ColorGroup.Inactive
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xfff5f5f5))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xffececec))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xffd4d4d4))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xd8000000))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff0000ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xffa9a9a9))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3f000000))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xd8000000))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xffececec))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xd8000000))
    

def DarkPaletteWindows(wgt):
    pal = wgt.palette()
    cg = QPalette.ColorGroup.Active
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xff989898))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xff171717))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xff314f78))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff3586ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xff242424))
    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xd8ffffff))

    cg = QPalette.ColorGroup.All
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xff989898))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xff171717))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xff314f78))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff3586ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xff242424))
#    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xd8ffffff))

    cg = QPalette.ColorGroup.Current
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xff989898))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xff171717))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xff314f78))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff3586ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xff242424))
#    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xd8ffffff))

    cg = QPalette.ColorGroup.Disabled
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xff989898))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xff363636))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff0000ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xff242424))
    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0x3fffffff))

    cg = QPalette.ColorGroup.Inactive
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xff989898))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xff171717))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffbfbfbf))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xff363636))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xff373737))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff0000ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xff242424))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xd8ffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0x3fffffff))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xff323232))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xd8ffffff))
    wgt.setPalette(pal)

def LightPaletteWindows(wgt):
    pal = wgt.palette()
    cg = QPalette.ColorGroup.Active
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,    QColor(0xfff5f5f5))
    pal.setColor(cg, QPalette.ColorRole.Base,             QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.BrightText,       QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Button,           QColor(0xfff0f0f0))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,       QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Dark,             QColor(0xffa0a0a0))
    pal.setColor(cg, QPalette.ColorRole.Highlight,        QColor(0xff0078d7))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText,  QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Light,            QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Link,             QColor(0xff0000ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,      QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,              QColor(0xffa0a0a0))
    pal.setColor(cg, QPalette.ColorRole.NColorRoles,      QColor(0xff787878))
    pal.setColor(cg, QPalette.ColorRole.NoRole,           QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText,  QColor(0x80000000))
    pal.setColor(cg, QPalette.ColorRole.Shadow,           QColor(0xff696969))
    pal.setColor(cg, QPalette.ColorRole.Text,             QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,      QColor(0xffffffdc))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,      QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,           QColor(0xfff0f0f0))
    pal.setColor(cg, QPalette.ColorRole.WindowText,       QColor(0xff000000))

    cg = QPalette.ColorGroup.All   #brush: Unknown ColorGroup: 5
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xfff5f5f5))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xfff0f0f0))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffa0a0a0))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xff0078d7))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff0000ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xffa0a0a0))
#    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0xff787878))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x80000000))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff696969))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0xffffffdc))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xfff0f0f0))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xff000000))

    cg = QPalette.ColorGroup.Current
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xfff5f5f5))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xfff0f0f0))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffa0a0a0))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xff0078d7))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff0000ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xffa0a0a0))
#    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0xff787878))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x80000000))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff696969))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0xffffffdc))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xfff0f0f0))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xff000000))
    
    cg = QPalette.ColorGroup.Disabled
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xfff5f5f5))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xfff0f0f0))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xfff0f0f0))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xff787878))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffa0a0a0))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xff0078d7))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff0000ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xffa0a0a0))
    pal.setColor(cg, QPalette.ColorRole.NColorRoles,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x80000000))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xff787878))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0xffffffdc))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xfff0f0f0))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xff787878))

    cg = QPalette.ColorGroup.Inactive
    pal.setColor(cg, QPalette.ColorRole.AlternateBase,   QColor(0xfff5f5f5))
    pal.setColor(cg, QPalette.ColorRole.Base,            QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.BrightText,      QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Button,          QColor(0xfff0f0f0))
    pal.setColor(cg, QPalette.ColorRole.ButtonText,      QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Dark,            QColor(0xffa0a0a0))
    pal.setColor(cg, QPalette.ColorRole.Highlight,       QColor(0xfff0f0f0))
    pal.setColor(cg, QPalette.ColorRole.HighlightedText, QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Light,           QColor(0xffffffff))
    pal.setColor(cg, QPalette.ColorRole.Link,            QColor(0xff0000ff))
    pal.setColor(cg, QPalette.ColorRole.LinkVisited,     QColor(0xffff00ff))
    pal.setColor(cg, QPalette.ColorRole.Mid,             QColor(0xffa0a0a0))
    pal.setColor(cg, QPalette.ColorRole.NoRole,          QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.PlaceholderText, QColor(0x80000000))
    pal.setColor(cg, QPalette.ColorRole.Shadow,          QColor(0xff696969))
    pal.setColor(cg, QPalette.ColorRole.Text,            QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.ToolTipBase,     QColor(0xffffffdc))
    pal.setColor(cg, QPalette.ColorRole.ToolTipText,     QColor(0xff000000))
    pal.setColor(cg, QPalette.ColorRole.Window,          QColor(0xfff0f0f0))
    pal.setColor(cg, QPalette.ColorRole.WindowText,      QColor(0xff000000))
    wgt.setPalette(pal)

             
def _DumpPalette(pal):
    for clrgrp in (QPalette.ColorGroup.Active,
                   QPalette.ColorGroup.All,
                   QPalette.ColorGroup.Current,
                   QPalette.ColorGroup.Disabled,
                   QPalette.ColorGroup.Inactive,
                   QPalette.ColorGroup.NColorGroups):
        DumpPaletteGroup(pal, clrgrp)


def _DumpPaletteGroup(pal, clrGrp):
    print(clrGrp.name)
#    c = pal.color(clrGrp, QPalette.ColorRole.Accent)
#    print(f"    Accent: {c}")
    c = pal.color(clrGrp, QPalette.ColorRole.AlternateBase)
    print(f"    AlternateBase:   {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.Base)
    print(f"    Base:            {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.BrightText)
    print(f"    BrightText:      {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.Button)
    print(f"    Button:          {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.ButtonText)
    print(f"    ButtonText:      {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.Dark)
    print(f"    Dark:            {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.Highlight)
    print(f"    Highlight:       {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.HighlightedText)
    print(f"    HighlightedText: {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.Light)
    print(f"    Light:           {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.Link)
    print(f"    Link:            {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.LinkVisited)
    print(f"    LinkVisited:     {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.Mid)
    print(f"    Mid:             {hex(c.rgba())}")
    if clrGrp != QPalette.ColorGroup.Inactive:
        c = pal.color(clrGrp, QPalette.ColorRole.NColorRoles)
        print(f"    NColorRoles:     {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.NoRole)
    print(f"    NoRole:          {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.PlaceholderText)
    print(f"    PlaceholderText: {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.Shadow)
    print(f"    Shadow:          {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.Text)
    print(f"    Text:            {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.ToolTipBase)
    print(f"    ToolTipBase:     {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.ToolTipText)
    print(f"    ToolTipText:     {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.Window)
    print(f"    Window:          {hex(c.rgba())}")
    c = pal.color(clrGrp, QPalette.ColorRole.WindowText)
    print(f"    WindowText:      {hex(c.rgba())}")


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    print(f"AffectiveTheme: {AffectiveTheme(app)}")
    #app.applicationStateChanged.connect(AppStateChangeCB)

#    pal = app.palette()
#    _DumpPalette(pal)
    
#    mainWin = MainWin()
#    mainWin.show()
    
#    status = app.exec()
#    sys.exit(status)
