import os
import curses


class ProgressBar:
    currentPercentage = 0
    currentValue = 0
    barWidth = 0
    maxValue = 100
    barName = 'Process'

    def __init__(self, name: str = 'Process', max_val: int = 100, width: int = -1):
        """
        Initializes the Progressbar
        :param name: str, default: 'Process'. Name that should be displayed with the processbar.
        :param max_val: int, default: 100. The amount where the processbar should be at 100%.
        :param width: int, default: -1. Width of the processbar. Set to -1 for full terminal width, else it has to be at least 1
        :return:
        """
        self.barName = name
        self.maxValue = max_val

        if width > 0:
            self.barWidth = width
        elif width == -1:
            max_width = os.get_terminal_size().columns
            self.barWidth = max_width - (len(name) + 19)
        else:
            raise Exception('Width has to be above 1 or exactly -1 for autoWidth')

        self.print_bar()

    def update_bar(self, value: int = 0):
        """
        Updates the values and reprints the Progressbar
        :param value: int, default: 0. The new value that should be displayed
        :return:
        """
        self.currentValue = value
        self.currentPercentage = float(value) * 100 / self.maxValue
        self.print_bar()

    def print_bar(self):
        """
        Prints the bar
        :return:
        """
        arrow = '=' * int(self.currentPercentage / 100 * self.barWidth - 1) + '>'
        spaces = ' ' * (self.barWidth - len(arrow))

        print('%s Progress: [%s%s] %d %%' % (self.barName, arrow, spaces, self.currentPercentage), end='\r')

    def end_bar(self):
        """
        Prints the bar with 100% and starts a newline
        :return:
        """
        print('%s Progress: [%s] %d %%' % (self.barName, '=' * int(self.barWidth), 100))


class AdvancedStatusWindow:
    types_with_max = ['ProgressBar', 'Percentage', 'Division']
    types_without_max = ['Counter', 'Status']
    attributes = {}
    rows = 0
    columns = 0
    window = None
    logfile = None
    header = 'My Advanced Status Window'
    half_header_len = len(header) / 2

    def __init__(self, header, log: str = '/var/log/coolOutput.log'):
        """
        Initializes the Advanced Status Window. Also opens the window. Add a log path if you want to log the data.
        :param header: str, default: 'My Advanced Status Window'. Header for the window
        :param log: str, default: '/var/log/coolOutput.log'. Path to the logfile.
        :return:
        """
        self.logfile = open(log, "a")
        self.header = header
        self.half_header_len = len(header) / 2

        self.window = curses.initscr()
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.rows, self.columns = self.window.getmaxyx()

    def add_attribute(self, name: str = 'Process', type_of: str = 'Counter', islogged: bool = False, max_value: int = 0):
        """
        Create a new attribute you want to track
        :param name: str, default: 'Process'. Name of the new attribute. Has to be unique
        :param type_of: str, default: 'Counter'. Style of the attribute output. Possibilities are 'ProgressBar',
        'Percentage', 'Division', 'Counter', 'Status'
        :param islogged: bool, default: False. Set to true if you want to log this attribute.
        :param max_value: int, default: 0. Highest expected value. Only needed for 'ProgressBar', 'Percentage',
        'Division'
        :return:
        """
        if name in self.attributes:
            raise Exception(f'{name} already exists')

        if type_of in self.types_with_max:
            if type_of == 'ProgressBar':
                self.attributes[name] = {'type': type_of,
                                         'value': 0,
                                         'islogged': islogged,
                                         'maxValue': max_value,
                                         'barWidth': self.columns - (len(name) + 10)}
            else:
                self.attributes[name] = {'type': type_of,
                                         'value': 0,
                                         'islogged': islogged,
                                         'maxValue': max_value}
        elif type_of in self.types_without_max:
            self.attributes[name] = {'type': type_of,
                                     'islogged': islogged,
                                     'value': 0}
        else:
            raise Exception(f'{type_of} is not a valid type of attribute')

    def add_to_log (self, name: str = 'Process', value=0):
        self.logfile.write(f'{name}: {value}')


    def update_attribute(self, name: str = 'Process', value=0):
        """
        Updates the value of one attribute, then renders the new text
        :param name: str, default: 'Process'. Name of the attribute you want to update
        :param value: default: 0. Value of the attribute you want to update
        :return:
        """
        if name not in self.attributes:
            raise Exception(f'{name} isn\'t a attribute')

        self.attributes[name]['value'] = value
        if self.attributes[name]['islogged']:
            self.add_to_log(name, value)
        self.update_window()

    def update_many(self, attr: dict = None):
        """
        Updates the values of multiple attributes, then renders the new text
        :param attr: dict, default: None. Dictionary of attribute_name, value pairs
        :return:
        """
        if attr is None:
            return
        for name in attr:
            if name not in self.attributes:
                raise Exception(f'{name} isn\'t a attribute')
            if self.attributes[name]['islogged']:
                self.add_to_log(name, attr[name])
            self.attributes[name]['value'] = attr[name]
        self.update_window()

    def update_window(self):
        """
        Renders the window text, with the newest values
        :return:
        """
        self.rows, self.columns = self.window.getmaxyx()
        self.window.clear()
        i = 4
        x = (self.columns / 2) - self.half_header_len
        self.window.addstr(2, x, self.header, curses.color_pair(2) | curses.A_BOLD)
        for name in self.attributes:
            if i > self.rows:
                break
            current = self.attributes[name]
            if current['type'] == 'Division':
                self.window.addstr(i, 0, '%s: %d/%d' % (name, current['value'], current['maxValue']), curses.color_pair(1))
            elif current['type'] == 'ProgressBar':
                percentage = float(current['value']) * 100 / current['maxValue']
                arrow = '=' * int(percentage / 100 * current['barWidth'] - 1) + '>'
                spaces = ' ' * (current['barWidth'] - len(arrow))
                self.window.addstr('%s: [%s%s] %d %%' % (name, arrow, spaces, percentage), curses.color_pair(1))
            elif current['type'] == 'Percentage':
                self.window.addstr(i, 0, '%s: %d %%' % (name, float(current['value']) * 100 / current['maxValue']), curses.color_pair(1))
            else:
                self.window.addstr(i, 0, '%s: %s' % (name, current['value']), curses.color_pair(1))
            i += 1
        self.window.refresh()

    def close_window(self):
        """
        Closes the window.
        :return:
        """
        self.logfile.close()
        self.reset_window()
        curses.endwin()

    def reset_window(self):
        """
        Resets the window and removes all attributes
        :return:
        """
        attributes = {}
        self.window.clear()
