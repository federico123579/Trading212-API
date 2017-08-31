# CONSTANTS
CYAN = '\033[96m'
PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
WHITE = '\033[0m'
MAGENTA = '\033[35m'
BOLD = '\033[01m'
UNDERLINE = '\033[04m'


# COLOR FUNCTIONS
def bold(string):
    return BOLD + str(string) + WHITE
def underline(string):
    return UNDERLINE + str(string) + WHITE
def cyan(string):
    return CYAN + str(string) + WHITE
def purple(string):
    return PURPLE + str(string) + WHITE
def blue(string):
    return BLUE + str(string) + WHITE
def green(string):
    return GREEN + str(string) + WHITE
def red(string):
    return RED + str(string) + WHITE
def yellow(string):
    return YELLOW + str(string) + WHITE
def white(string):
    return WHITE + str(string) + WHITE


class printer(object):
    @staticmethod
    def header(string):
        return bold(blue('------ ' + str(string.upper()) + ' ------'))

    @staticmethod
    def process(string=''):
        return '[' + cyan('+') + '] ' + str(string)

    @staticmethod
    def info(string=''):
        return '[' + blue('#') + '] ' + str(string)

    @staticmethod
    def warning(string=''):
        return '[' + yellow('-') + '] ' + str(string)

    @staticmethod
    def error(string=''):
        return '[' + magenta('=') + '] ' + str(string)

    @staticmethod    
    def critical(string=''):
        return '[' + red('~') + '] ' + str(string)

    @staticmethod
    def user_input(string=''):
        return '[' + green('$') + '] ' + str(string)