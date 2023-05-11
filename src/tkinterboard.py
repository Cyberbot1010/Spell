import tkinter as tk
from tkinter.font import Font
from src.baseui import BaseUI


class BoardMenu:
    """Represents the contextual menu in GUI"""
    def __init__(self, board: 'TkinterBoard', entry: 'BoardEntry') -> None:
        self.board = board
        app = board.app

        self.menu = tk.Menu(app.root, tearoff = 0)

        self.menu.add_command(label="2X", command=lambda: self.board.mult.set_mult_word(entry.cord))
        self.menu.add_command(label="DL", command=lambda: self.board.mult.set_mult_DL(entry.cord))
        self.menu.add_command(label="TL", command=lambda: self.board.mult.set_mult_TL(entry.cord))
        self.menu.add_separator()
        self.menu.add_command(label="Remove bonus", command=lambda: self.board.mult.remove_mult())


class BoardEntry:
    """Represents a square tile in GUI"""
    def __init__(self, board: 'TkinterBoard', aux_cord: int) -> None:
        self.board = board
        app = board.app

        (x, y) = aux_cord % 5, aux_cord // 5
        self.cord = (x, y)
        self.menu = BoardMenu(board, self)

        def on_validate(input: str, aux_cord: int) -> bool:
            """Validate the value in the entry"""
            aux_cord = (int(aux_cord) + 1) % 25
            cord = (aux_cord % 5, aux_cord // 5)
            
            if len(input) == 1:
                board.inputs[cord].focus_set()
                board.inputs[cord].select_range(0, 'end')
            return True
        
        def do_popup(event) -> None:
            """Handle the popup event in the entry"""
            try:
                self.menu.menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.menu.menu.grab_release()

        board.tiles[self.cord] = tk.StringVar(app.root, value='')
        entry = tk.Entry(app.root, textvariable=board.tiles[self.cord], validate="key", highlightthickness=2)

        entry["borderwidth"] = "1px"
        entry["font"] = Font(family='Times',size=10)
        entry["fg"] = "#333333"
        entry["justify"] = "center"
        entry['validatecommand'] = (entry.register(on_validate), '%P', aux_cord)
        entry.place(x=app.xoff+x*32, y=app.yoff+y*32, width=32, height=32)
        entry.configure(highlightbackground="black", highlightcolor="black", font=('Roboto', 16))
        entry.bind("<Button-3>", do_popup)

        board.inputs[self.cord] = entry


class BoardLabel:
    """Represents a result label"""
    def __init__(self, board: 'TkinterBoard', num: int) -> None:
        self.board = board
        app = board.app

        self.label = tk.Label(app.root)
        self.label["borderwidth"] = "1px"
        self.label["font"] = Font(family='Times',size=14)
        self.label["fg"] = "#333333"
        self.label["justify"] = "center"
        self.label["text"] = f""
        self.label.place(x=320,y=10+num*22,width=250,height=25)
    
    def set_text(self, text: str) -> None:
        """Set text value of the label"""
        self.label["text"] = str(text)


class BoardButton:
    """Represents a button"""
    def __init__(self, board: 'TkinterBoard', text: str, num: int, command: callable) -> None:
        self.board = board
        app = board.app

        self.button = tk.Button(app.root)
        self.button["bg"] = "#e9e9ed"
        self.button["font"] = Font(family='Times',size=10)
        self.button["fg"] = "#000000"
        self.button["justify"] = "center"
        self.button["text"] = text
        self.button.place(x=app.xoff+num*80,y=app.yoff+160,width=80,height=25)
        self.button["command"] = command
        

class LabelHover:
    """Represent a hover event handler for result labels"""
    def __init__(self, board: 'TkinterBoard', label: BoardLabel, path: list) -> None:
        self.board = board
        self.label = label
        self.path = path

        self.label.label.bind('<Enter>', lambda _ : self.hover())
        self.label.label.bind('<Leave>', lambda _ : self.unhover())
    
    def font_conf(self, color: str) -> dict:
        """Get default font configuration"""
        return {
            "highlightbackground": color,
            "highlightcolor": color,
            "background": color,
            "font": ('Roboto', 20, tk.font.BOLD),
            "fg": "white"
        }

    def hover(self) -> None:
        """Handle hover event in the label"""
        for tile in self.path:
            if tile.swap:
                self.board.inputs[tile.cord].configure(**self.font_conf("red"))
                self.board.tiles[tile.cord].set(tile.letter)
            else:
                self.board.inputs[tile.cord].configure(**self.font_conf("blue"))
        self.label.label.focus_set()

    def unhover(self) -> None:
        """handle unhover event in the label"""
        for tile in self.path:
            self.board.inputs[tile.cord].configure(highlightbackground="black", highlightcolor="black", background="white", font=('Roboto', 16, tk.font.NORMAL), fg="black")
            self.board.tiles[tile.cord].set(self.board.app.gameboard.tiles[tile.cord].letter)
            self.board.mult.configure_mult()


class MultHandler:
    """Handle Spellcast word & letter multipliers"""
    def __init__(self, board: 'TkinterBoard') -> None:
        self.board: TkinterBoard = board

        self.mult_cord: tuple = None
        self.DL_cord: tuple = None
        self.TL_cord: tuple = None
    
    def font_conf(self, color: str) -> dict:
        """Get default font configuration"""
        return {
            "highlightbackground": color,
            "highlightcolor": color,
            "background": "white",
            "font": ('Roboto', 16, tk.font.NORMAL),
            "fg": "black"
        }
    
    def set_mult_word(self, cord: tuple) -> None:
        """Set a mult_word in a tile"""
        if self.mult_cord != None:
            self.board.inputs[self.mult_cord].configure(**self.font_conf("black"))

        self.mult_cord = cord
        self.board.inputs[self.mult_cord].configure(**self.font_conf("deep pink"))

    def set_mult_DL(self, cord: tuple) -> None:
        """Set a mult_DL in a tile"""
        if self.DL_cord != None:
            self.board.inputs[self.DL_cord].configure(**self.font_conf("black"))
        
        self.DL_cord = cord
        self.board.inputs[self.DL_cord].configure(**self.font_conf("gold"))

    def set_mult_TL(self, cord: tuple) -> None:
        """Set a mult_TL in a tile"""
        if self.TL_cord != None:
            self.board.inputs[self.TL_cord].configure(**self.font_conf("black"))
        
        self.TL_cord = cord
        self.board.inputs[self.TL_cord].configure(**self.font_conf("gold"))

    def configure_mult(self) -> None:
        """Change colors of a tile based in the multipliers"""
        if self.mult_cord != None:
            self.board.inputs[self.mult_cord].configure(**self.font_conf("deep pink"))
        if self.DL_cord != None:
            self.board.inputs[self.DL_cord].configure(**self.font_conf("gold"))
        if self.TL_cord != None:
            self.board.inputs[self.TL_cord].configure(**self.font_conf("gold"))
        
    def remove_mult(self) -> None:
        """Remove colors of a tile"""
        if self.mult_cord != None:
            self.board.inputs[self.mult_cord].configure(**self.font_conf("black"))
        if self.DL_cord != None:
            self.board.inputs[self.DL_cord].configure(**self.font_conf("black"))
        if self.TL_cord != None:
            self.board.inputs[self.TL_cord].configure(**self.font_conf("black"))
        
        self.mult_cord = None
        self.DL_cord = None
        self.TL_cord = None


class TkinterBoard:
    """Represents a Tkinter Board with his logic"""
    def __init__(self, app: BaseUI) -> None:
        self.app: BaseUI = app
        self.mult: MultHandler = MultHandler(self)

        self.entry: list = []
        self.labels: list = []
        self.buttons: list = []
        
        self.inputs: dict = {}
        self.tiles: dict = {}
        
        for aux_cord in range(25):
            self.entry += [BoardEntry(self, aux_cord)]

        for num in range(10):
            self.labels += [BoardLabel(self, num)]
        
        self.buttons += [BoardButton(self, "Normal", 0, lambda: self.button_command(swap=False))]
        self.buttons += [BoardButton(self, "Swap", 1, lambda: self.button_command(swap=True))]
    
    def button_command(self, swap: bool) -> None:
        """Execute SpellSolver when a button is pressed"""
        gameboard_string = "".join([t.get().lower() for t in self.tiles.values()])
        self.app.gameboard.load(gameboard_string)

        if self.mult.mult_cord != None:
            self.app.gameboard.set_mult_word(self.mult.mult_cord)
        if self.mult.DL_cord != None:
            self.app.gameboard.set_mult_letter(self.mult.DL_cord, 2)
        if self.mult.TL_cord != None:
            self.app.gameboard.set_mult_letter(self.mult.TL_cord, 3)
        
        word_list = self.app.solve(swap)
        for i, result in enumerate(word_list):
            if i >= len(self.labels):
                break
            self.labels[i].set_text(result[:2])
            LabelHover(self, self.labels[i], result[-1])