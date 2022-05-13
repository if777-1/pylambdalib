import curses

class CursesManager:

    def __init__(self, menu=None):
        if menu is None:
            menu = {}
        self.menu = menu
        curses.wrapper(self.start)

    def start(self,stdscr):
        # turn off cursor blinking
        curses.curs_set(0)
        # color scheme for selected row
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # specify the current selected row
        current_row = 0
        # print the menu
        self.print_menu(stdscr, current_row)

        while 1:
            key = stdscr.getch()

            if key == curses.KEY_UP:
                if current_row == 0:
                    current_row = len(self.menu) - 1
                else:
                    current_row -= 1
            elif key == curses.KEY_DOWN:
                if current_row == len(self.menu) - 1:
                    current_row = 0
                else:
                    current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.print_select(stdscr, current_row)
                stdscr.getch()
                # if user selected last row, exit the program
                if current_row == len(self.menu) - 1:
                    break

            self.print_menu(stdscr, current_row)

    def print_menu(self,stdscr, selected_row_idx):
        stdscr.clear()
        stdscr.addstr("Redis Tools v1.0: \n")
        for idx, row in enumerate(self.menu):
            x = 0
            y = len(self.menu) // 2 + idx
            if idx == selected_row_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)
        stdscr.refresh()

    def print_select(self,stdscr, current_row):
        stdscr.clear()
        stdscr.addstr(self.menu[current_row] + ":\n")
        stdscr.refresh()

c = CursesManager(menu = ['Generar txt para cambiar id de companias',
        'ID maximo',
        'IDs usados',
        'Eliminar val',
        'Generar DXF',
        'Generar KMZ',
        'Dar de alta compania',
        'Dar de alta usuarios',
        'Consultar usuarios',
        'Verificar base de datos',
        'Cambiar configuracion',
        'Salir'
        ])