import curses

class CursesHandler:
    def __init__(self,stdscr):
        self.stdscr = stdscr

    def clear_screen(self):
        self.stdscr.clear()
        self.stdscr.refresh()

    def wait_for_input(self):
        self.stdscr.getch()

    def rewrite_line(self, text):
        self.stdscr.addstr("\r"+text)
        self.stdscr.refresh()

    def println(self,text):
        self.stdscr.addstr(text+"\n")
        self.stdscr.refresh()

    def choice_input(self,initial_text,menu):
        curses.curs_set(0)
        # color scheme for selected row
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # specifies the current selected row
        current_column = 0
        self.println(initial_text)
        self.print_choice_input(current_column,menu)
        while True:
            key = self.stdscr.getch()

            if key == curses.KEY_LEFT:
                if current_column == 0:
                    current_column = len(menu)-1
                else:
                    current_column -= 1
            elif key == curses.KEY_RIGHT:
                if current_column == len(menu)-1:
                    current_column = 0
                else:
                    current_column += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.stdscr.addstr('\n')
                return menu[current_column]
            self.print_choice_input(current_column,menu)

    def print_choice_input(self, selected_column_idx,menu):
        self.rewrite_line('')
        for idx, row in enumerate(menu):
            count = sum(map(lambda a:len(a)+2,menu[:idx]))
            self.stdscr.refresh()
            y,_ = self.stdscr.getyx()
            x = 2 + count
            if idx == selected_column_idx:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)
        self.stdscr.refresh()

    def general_input(self,input_message,default,acceptance_condition):
        curses.curs_set(1)
        self.stdscr.addstr(input_message)
        d = str(default)
        self.stdscr.addstr(d)
        self.stdscr.refresh()
        c = self.stdscr.getkey()
        while c != '\n':
            if acceptance_condition(c):
                self.stdscr.addstr(c)
                d += c
            # if there is nothing else to erase, don't erase anything
            elif c == 'KEY_BACKSPACE' and len(d)>0:
                self.stdscr.addstr('\b')
                self.stdscr.addstr(' ')
                self.stdscr.addstr('\b')
                d = d[:-1]
            c = self.stdscr.getkey()
        self.stdscr.addstr('\n')
        curses.curs_set(0)
        return d

    def str_input(self,input_message,default=''):
        return self.general_input(input_message,default,lambda x:len(x) == 1)

    def numeric_input(self,input_message,default=''):
        return self.general_input(input_message,default,lambda x: x.isdigit())

    def main_menu(self,txt,menu, select_handler):
        # turn off cursor blinking
        curses.curs_set(0)
        # color scheme for selected row
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # specify the current selected row
        current_row = 0
        # print the menu
        self.print_menu(current_row,txt,menu)
        while True:
            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                if current_row == 0:
                    current_row = len(menu) - 1
                else:
                    current_row -= 1
            elif key == curses.KEY_DOWN:
                if current_row == len(menu) - 1:
                    current_row = 0
                else:
                    current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.clear_screen()
                self.stdscr.refresh()
                self.print_select(current_row, select_handler)
            self.print_menu(current_row,txt,menu)
            self.stdscr.refresh()

    def menu(self,txt,menu):
        # turn off cursor blinking
        curses.curs_set(0)
        # color scheme for selected row
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # specify the current selected row
        current_row = 0
        # print the menu
        self.print_menu(current_row,txt,menu)
        while True:
            key = self.stdscr.getch()

            if key == curses.KEY_UP:
                if current_row == 0:
                    current_row = len(menu) - 1
                else:
                    current_row -= 1
            elif key == curses.KEY_DOWN:
                if current_row == len(menu) - 1:
                    current_row = 0
                else:
                    current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.clear_screen()
                self.stdscr.refresh()
                return current_row
            self.print_menu(current_row,txt,menu)
            self.stdscr.refresh()

    def print_menu(self, selected_row_idx,txt,menu):
        self.stdscr.clear()
        self.println(txt)
        for idx, row in enumerate(menu):
            x = 0
            y = 2 + idx
            if idx == selected_row_idx:
                self.stdscr.attron(curses.color_pair(1))
                self.stdscr.addstr(y, x, row)
                self.stdscr.attroff(curses.color_pair(1))
            else:
                self.stdscr.addstr(y, x, row)
        self.stdscr.refresh()

    # una vez que se selecciona una de las opciones, se llama a la funcion pasada
    # y se le pasa por parametro la fila elegida
    def print_select(self,current_row, select_handler):
        self.stdscr.clear()
        self.stdscr.refresh()
        self.stdscr.scrollok(True)
        select_handler(current_row)
        self.stdscr.refresh()