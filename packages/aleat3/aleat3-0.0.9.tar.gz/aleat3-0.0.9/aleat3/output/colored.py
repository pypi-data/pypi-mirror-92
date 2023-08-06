"""
Use console-colored functions.

This file uses Colorama (http://pypi.org/project/colorama) for colored output.
"""

__all__ = ["UNABLE"]

error_text = """Unable to load Colorama package. Some fuctions may not run correctly
without this function. You can download the package at the PyPi page:

            http://pypi.org/project/colorama"""

try:
    from colorama import Fore, Back, Style, init
    __all__ = __all__ + ["output_red", "output_green", "output_yellow"]
    UNABLE = True
    def output_red(message):
        #if not isinstance(message, "str"):
            #raise TypeError("Can only use string data, not %s" % type(message))
        init()
        print(Fore.RED + message)
        print(Style.RESET_ALL)

    def output_yellow(message):
        #if not isinstance(message, "str"):
            #raise TypeError("Can only use string data, not %s" % type(message))
        init()
        print(Fore.YELLOW + message)
        print(Style.RESET_ALL)

    def output_green(message):
        #if not isinstance(message, "str"):
            #raise TypeError("Can only use string data, not %s" % type(message))
        init()
        print(Fore.GREEN + message)
        print(Style.RESET_ALL)
except:
    print(error_text)
    UNABLE = False
    def output_red(message=None):
        print(error_text)

    def output_green(message=None):
        print(error_text)

    def output_yellow(message=None):
        print(Error_text)


if __name__ == '__main__':
    import time
    output_red("Red output")
    output_green("Green output")
    output_yellow("Yellow output")
    print("Unable?:", UNABLE)
    time.sleep(1)
