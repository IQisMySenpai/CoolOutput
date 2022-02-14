import sys, os
import curses


class ProgressBar:
    currentPercentage = 0
    currentValue = 0
    barWidth = 0
    maxValue = 100
    barName = 'Process'

    def __init__(self, name: str = 'Process', max: int = 100, width: int = -1):
        """
        Initializes the Progressbar
        :param name: str, default: 'Process'. Name that should be displayed with the processbar.
        :param max: int, default: 100. The amount where the processbar should be at 100%.
        :param width: int, default: -1. Width of the processbar. Set to -1 for full terminal width, else it has to be at least 1
        :return: None
        """
        self.barName = name
        self.maxValue = max

        if width > 0:
            self.barWidth = width
        elif width == -1:
            max_width = os.get_terminal_size().columns
            self.barWidth = max_width - (len(name) + 19)
        else:
            raise Exception("Width has to be above 1 or exactly -1 for autoWidth")

        self.print_bar()

    def update_bar(self, value: int = 0):
        """
        Updates the values and reprints the Progressbar
        :param value: int, default: 0. The new value that should be displayed
        :return: None
        """
        self.currentValue = value
        self.currentPercentage = float(value) * 100 / self.maxValue
        self.print_bar()

    def print_bar(self):
        """
        Prints the bar
        :return: None
        """
        arrow = '=' * int(self.currentPercentage / 100 * self.barWidth - 1) + '>'
        spaces = ' ' * (self.barWidth - len(arrow))

        print('%s Progress: [%s%s] %d %%' % (self.barName, arrow, spaces, self.currentPercentage), end='\r')

    def end_bar(self):
        """
        Prints the bar with 100% and starts a newline
        :return: None
        """
        print('%s Progress: [%s] %d %%' % (self.barName, '=' * int(self.barWidth), 100))

