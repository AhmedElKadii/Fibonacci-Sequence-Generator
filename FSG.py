import tkinter as tk
import turtle
from math import sqrt

class FibonacciSpiral:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x1000")
        
        self.canvas = tk.Canvas(self.root, height=570, width=800, bg='white')

        self.show_boxes: bool = True
        
        self.main_menu_frame = tk.Frame(self.root)
        self.settings_menu_frame = tk.Frame(self.root)

        self.length_entry = tk.Entry(self.settings_menu_frame, font=('Helvetica', 15))
        self.speed_slider = tk.Scale(self.settings_menu_frame, from_=1, to=10, orient='horizontal', length=200)

        self.n_frame = tk.Frame(self.settings_menu_frame)

        self.show_boxes_checkbox = tk.Checkbutton(self.settings_menu_frame, text="Show Boxes", font=('Helvetica', 15))

        self.n_entry = tk.Entry(self.n_frame, font=('Helvetica', 15))
        self.n_plus_button = tk.Button(self.n_frame, text="+", font=('Helvetica', 15), width=5, height=1, command=self.add_n)
        self.n_minus_button = tk.Button(self.n_frame, text="-", font=('Helvetica', 15), width=5, height=1, command=self.subtract_n)
        
        self.checkbox_var = tk.BooleanVar()

        self.has_drawn: bool = False

        self.cursor = turtle.RawTurtle(self.canvas)
        self.cursor2 = turtle.RawTurtle(self.canvas)

        for t in (self.cursor, self.cursor2):
            t.speed(0)
            t.hideturtle()
        
        self.length = 5
        self.n = 4
        self.setup_main_menu()

    def setup_main_menu(self):
        """Setup the main menu frame."""
        self.root.title("Main Menu")

        title_label = tk.Label(self.main_menu_frame, text="Fibonacci Sequence Generator", font=('Helvetica', 24))
        title_label.pack(pady=20)

        start_button = tk.Button(self.main_menu_frame, text="Start Fibonacci Spiral", font=('Helvetica', 15),
                                 command=self.start_fibonacci_spiral, width=20, height=2)
        start_button.pack(pady=10)

        settings_button = tk.Button(self.main_menu_frame, text="Settings", font=('Helvetica', 15),
                                    command=self.setup_settings_menu, width=20, height=2)
        settings_button.pack(pady=10)

        exit_button = tk.Button(self.main_menu_frame, text="Exit", font=('Helvetica', 15), command=self.root.quit, width=20, height=2)
        exit_button.pack(pady=10)

        self.main_menu_frame.pack(expand=True)

    def setup_settings_menu(self):
        """Setup the settings menu frame."""
        self.settings_menu_frame.pack(expand=True)
        self.root.title("Settings")
        
        self.canvas.update()

        title_label = tk.Label(self.settings_menu_frame, text="Settings", font=('Helvetica', 24))
        title_label.pack(pady=20)

        length_label = tk.Label(self.settings_menu_frame, text="Length:", font=('Helvetica', 15))
        length_label.pack(pady=10)

        self.length_entry.pack(pady=10)


        checkbox = tk.Checkbutton(self.settings_menu_frame, text="Enable Boxes", variable=self.checkbox_var)
        checkbox.pack(pady=10)
        self.checkbox_var.set(True)

        self.speed_slider.pack(pady=10)

        n_label = tk.Label(self.settings_menu_frame, text="n:", font=('Helvetica', 15))
        n_label.pack(pady=10)

        self.n_frame.pack(pady=10)

        self.n_entry.pack(side='left')

        self.n_minus_button.pack(side='left')
        self.n_plus_button.pack(side='left')

        apply_button = tk.Button(self.settings_menu_frame, text="Apply", font=('Helvetica', 15),
                                 command=self.apply_settings, width=20, height=2)
        apply_button.pack(pady=10)

        back_button = tk.Button(self.settings_menu_frame, text="Back", font=('Helvetica', 15),
                                command=self.destroy_settings_menu, width=20, height=2)
        back_button.pack(pady=10)

    def destroy_settings_menu(self):
        """Destroy the settings menu frame."""
        self.settings_menu_frame.pack_forget()
        self.main_menu_frame.pack(expand=True)

    def apply_settings(self):
        """Apply the settings from the settings menu."""
        try:
            self.length = int(self.length_entry.get())
        except ValueError:
            print("Invalid length value, using default.")
            self.length = 5
        
        slider_value = self.speed_slider.get()

        if slider_value <= 2:
            turtle_speed = "slowest"
        elif slider_value <= 4:
            turtle_speed = "slow"
        elif slider_value <= 6:
            turtle_speed = "normal"
        elif slider_value <= 8:
            turtle_speed = "fast"
        else:
            turtle_speed = "fastest"

        for t in (self.cursor, self.cursor2):
            t.speed(turtle_speed)

        self.show_boxes = self.checkbox_var.get()

        try:
            self.n = int(self.n_entry.get())
        except ValueError:
            print("Invalid n value, using default.")
            self.n = 4
        
        self.settings_menu_frame.pack_forget()

    def add_n(self):
        """Increment the n value."""
        self.n += 1
        self.n_entry.delete(0, tk.END)
        self.n_entry.insert(0, str(self.n))

    def subtract_n(self):
        """Decrement the n value."""
        self.n -= 1
        self.n_entry.delete(0, tk.END)
        self.n_entry.insert(0, str(self.n))

    def setup_ui(self):
        """Setup the UI for the Fibonacci spiral screen."""
        self.main_menu_frame.pack_forget()
        self.canvas.pack(expand=True, fill='both')
        
        phi = (1 + sqrt(5)) / 2
        label = tk.Label(self.root, text=f"ø = {phi:.6f}", font=('Helvetica', 18))
        label.pack(pady=10)

        zoom_frame = tk.Frame(self.root)
        zoom_frame.pack(pady=5)

        zoom_in_button = tk.Button(zoom_frame, text="Zoom In", font=('Helvetica', 15), command=self.zoom_in)
        zoom_in_button.pack(side='left')

        zoom_out_button = tk.Button(zoom_frame, text="Zoom Out", font=('Helvetica', 15), command=self.zoom_out)
        zoom_out_button.pack(side='left')

        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        
    def fib(self, n: int) -> int:
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    
    def draw_square(self, l: int):
        for _ in range(4):
            self.cursor.forward(self.length * l)
            self.cursor.left(90)
    
    def draw_circle(self, r: int):
        self.cursor2.circle(self.length * r, 90)
    
    def draw_fib(self, n: int):
        self.has_drawn = False

        for t in (self.cursor, self.cursor2):
            t.clear()
            t.penup()
            t.goto(0, 0)
            t.pendown()

        for i in range(1, n+1):
            if i%4 == 1:
                if self.show_boxes == True:
                    self.draw_square(self.fib(i))
                self.draw_circle(self.fib(i))
            elif i%4 == 2:
                if self.show_boxes == True:
                    self.cursor.penup()
                    self.cursor.left(90)
                    self.cursor.forward(self.length*self.fib(i-1))
                    self.cursor.pendown()
                    self.cursor.right(90)
                    if self.fib(i) != self.fib(i-1):
                        self.cursor.penup()
                        self.cursor.left(180)
                        self.cursor.forward(self.length*(self.fib(i-3)+self.fib(i-4)))
                        self.cursor.right(180)
                        self.cursor.pendown()
                    self.draw_square(self.fib(i))
                self.cursor2.penup()
                self.cursor2.setheading(90)
                self.cursor2.pendown()
                self.draw_circle(self.fib(i))
            elif i%4 == 3:
                if self.show_boxes == True:
                    self.cursor.penup()
                    self.cursor.left(180)
                    self.cursor.forward(self.length*self.fib(i))
                    self.cursor.left(90)
                    if i != 3:
                        self.cursor.forward(self.length*(self.fib(i-3)+self.fib(i-4)))
                    else:
                        self.cursor.forward(self.length*self.fib(i)/2)
                    self.cursor.left(90)
                    self.cursor.pendown()
                    self.draw_square(self.fib(i))
                self.draw_circle(self.fib(i))
            elif i%4 == 0:
                if self.show_boxes == True:
                    self.cursor.penup()
                    self.cursor.right(90)
                    self.cursor.forward(self.length*self.fib(i))
                    self.cursor.left(90)
                    self.cursor.pendown()
                    self.draw_square(self.fib(i))
                self.cursor.penup()
                self.cursor.forward(self.length*self.fib(i))
                self.cursor.pendown()
                self.draw_circle(self.fib(i))

        self.has_drawn = True

    def redraw(self):
        self.canvas.delete("all")
        self.draw_fib(self.n)

    def zoom_in(self):
        if self.has_drawn:
            self.length += 3
            self.redraw()

    def zoom_out(self):
        if self.has_drawn:
            self.length -= 3
            self.redraw()

    def start_fibonacci_spiral(self):
        """Switch to the Fibonacci spiral screen from the main menu."""
        self.setup_ui()
        self.settings_menu_frame.pack_forget()
        self.settings_menu_frame.pack_forget()
        
        self.root.title("Fibonacci Sequence Generator")

        self.draw_fib(self.n)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FibonacciSpiral()
    app.run()
