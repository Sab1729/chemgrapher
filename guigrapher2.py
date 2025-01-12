from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageTk, Image

button_color = "#cde1eb"

# Main window 
root = Tk()
root.title("Chemistry Grapher")
root.geometry("500x600")
root.configure(bg="#c9aafb")
root.resizable(False, False)

#logo
logo = Image.open("image.png")
logo = logo.resize((32,32))
logo_tk = ImageTk.PhotoImage(logo)

root.iconphoto(False, logo_tk)

# Variables for bestfit_line
x_count = 0
x_start = 0
x_updat = 0
y_entries = []

# Scrollable Frame for input entries
scroll_canvas = Canvas(root, height=400, width=450, bg="#c9aaff")
scroll_canvas.grid(row=1, column=0, padx=10, pady=10)

scroll_frame = Frame(scroll_canvas, bg="#c9aaff")
scroll_frame.grid(row=0, column=0)

scrollbar = Scrollbar(root, orient="vertical", command=scroll_canvas.yview)
scrollbar.grid(row=1, column=1, sticky="ns")
scroll_canvas.configure(yscrollcommand=scrollbar.set)

# Update scroll region after adding widgets
def update_scroll_region(event):
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

scroll_frame.bind("<Configure>", update_scroll_region)
scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

# Choice Frame
choise_frame = LabelFrame(root, text="", padx=10, pady=10, bg="#c9aafb", font=("Arial", 12, "bold"))
choise_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Dropdown and Label
clicked = StringVar()
options = ["Select", "Bestfit-line", "Curve"]
clicked.set(options[0])

label_for_dd = Label(choise_frame, text="Please select the type of plotting:", font=("Arial", 10), bg="#c9aabb")
label_for_dd.grid(row=0, column=0, padx=10, pady=5)

drop_down = OptionMenu(choise_frame, clicked, *options)
drop_down.config(width=15, font=("Arial", 10), bg="#cfaaff")
drop_down.grid(row=0, column=1, padx=10, pady=5)

# Function to handle the conversion to float with error handling
def gsb(x_count_get, x_start_get, x_updat_get, title_get, x_label_get, y_label_get):
    global x_count, x_start, x_updat, y_entries

    try:
        x_count = int(x_count_get.get())  
        x_start = float(x_start_get.get())  
        x_updat = float(x_updat_get.get()) 
        title = title_get.get()  
        x_label = x_label_get.get()  
        y_label = y_label_get.get()  
        
        #messagebox.showinfo("Success", f"x_count: {x_count}, x_start: {x_start}, x_updat: {x_updat}")

        # Generate dynamic x labels and y entry boxes
        for widget in scroll_frame.winfo_children():
            widget.destroy()

        y_entries = []  
        x_values = [x_start + i * x_updat for i in range(x_count)]  

        for i, x_val in enumerate(x_values):
            Label(scroll_frame, text=f"x = {x_val:.2f}", bg="#ffffff", font=("Arial", 10)).grid(row=i, column=0, padx=10, pady=5)
            y_entry = Entry(scroll_frame)
            y_entry.grid(row=i, column=1, padx=10, pady=5)
            y_entries.append(y_entry)  # Store the entry widget for later retrieval

        # Button to generate the best-fit line
        Button(scroll_frame, text="Plot Best-Fit Line", command=lambda: plot_bestfit_line(title, x_label, y_label), bg=button_color, font=("Arial", 10, "bold")).grid(row=x_count, column=0, columnspan=2, pady=10)

        # Entry for known point
        Label(scroll_frame, text="Known Point X (Optional):", font=("Arial", 10), bg="#ffffff").grid(row=x_count + 1, column=0, padx=5, pady=5)
        point_x_entry = Entry(scroll_frame)
        point_x_entry.grid(row=x_count + 1, column=1, padx=5, pady=5)

        Label(scroll_frame, text="Known Point Y (Optional):", font=("Arial", 10), bg="#ffffff").grid(row=x_count + 2, column=0, padx=5, pady=5)
        point_y_entry = Entry(scroll_frame)
        point_y_entry.grid(row=x_count + 2, column=1, padx=5, pady=5)

        # Button to plot with known point
        Button(scroll_frame, text="Plot with Known Point", command=lambda: plot_bestfit_line(title, x_label, y_label, point_x_entry.get(), point_y_entry.get()), bg=button_color, font=("Arial", 10, "bold")).grid(row=x_count + 3, column=0, columnspan=2, pady=10)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values")

# Function to plot the best-fit line
def plot_bestfit_line(title, x_label, y_label, point_x=None, point_y=None):
    global x_count, x_start, x_updat, y_entries

    try:
        y_values = [float(entry.get()) for entry in y_entries]  # Retrieve y values from entries
        x_values = [x_start + i * x_updat for i in range(x_count)]  # Recalculate x values

        if len(y_values) != len(x_values):
            messagebox.showerror("Error", "Number of y-values does not match the number of x-values")
            return

        # Extend x values for best-fit line
        extended_x_values = [x_values[0] - x_updat] + x_values + [x_values[-1] + x_updat]
        
        # Calculate the best-fit line
        coefficients = np.polyfit(x_values, y_values, 1)
        poly_eq = np.poly1d(coefficients)
        
        # Plot the points and the best-fit line
        plt.scatter(x_values, y_values, color='blue')  # Removed label to exclude it from the legend
        plt.plot(extended_x_values, poly_eq(extended_x_values), color='red')  # Removed label for best-fit line

        # Check if a known point is provided
        if point_x or point_y:
            if point_x:  # If known x is provided
                point_x_value = float(point_x)
                point_y_value = poly_eq(point_x_value)
            elif point_y:  # If known y is provided
                point_y_value = float(point_y)
                point_x_value = (point_y_value - coefficients[1]) / coefficients[0]  # Rearrange y = mx + c to find x
            
            # Plot the known point
            plt.scatter(point_x_value, point_y_value, color='green', s=100)

            # Plot dotted lines to axes
            plt.axvline(point_x_value, color='green', linestyle='--')  # Vertical line
            plt.axhline(point_y_value, color='green', linestyle='--')  # Horizontal line

            # Annotate the known point coordinates
            plt.text(point_x_value, point_y_value, f'({point_x_value:.2f}, {point_y_value:.2f})', color='green', fontsize=12, ha='right')

        # Plot formatting
        plt.title(rf"{title}")
        plt.xlabel(rf"{x_label}")
        plt.ylabel(rf"{y_label}")
        plt.grid(True)

        plt.show()

    except ValueError:
        messagebox.showerror("Invalid Input", "Please ensure all y-values are valid numbers")



def bestfit_line():
    for widget in scroll_frame.winfo_children():
        widget.destroy()

    # Labels and Entries for parameters
    Label(scroll_frame, text="Graph Title:", font=("Arial", 10), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
    title_entry = Entry(scroll_frame)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(scroll_frame, text="X-axis label:", font=("Arial", 10), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5)
    x_label_entry = Entry(scroll_frame)
    x_label_entry.grid(row=1, column=1, padx=5, pady=5)

    Label(scroll_frame, text="Y-axis label:", font=("Arial", 10), bg="#ffffff").grid(row=2, column=0, padx=5, pady=5)
    y_label_entry = Entry(scroll_frame)
    y_label_entry.grid(row=2, column=1, padx=5, pady=5)

    Label(scroll_frame, text="Number of X values:", font=("Arial", 10), bg="#ffffff").grid(row=3, column=0, padx=5, pady=5)
    X_count_get = Entry(scroll_frame)
    X_count_get.grid(row=3, column=1, padx=5, pady=5)

    Label(scroll_frame, text="Starting X value:", font=("Arial", 10), bg="#ffffff").grid(row=4, column=0, padx=5, pady=5)
    X_start_get = Entry(scroll_frame)
    X_start_get.grid(row=4, column=1, padx=5, pady=5)

    Label(scroll_frame, text="Update in X value:", font=("Arial", 10), bg="#ffffff").grid(row=5, column=0, padx=5, pady=5)
    X_updat_get = Entry(scroll_frame)
    X_updat_get.grid(row=5, column=1, padx=5, pady=5)

    # Submit Button
    submit_button = Button(scroll_frame, text="Submit", command=lambda: gsb(X_count_get, X_start_get, X_updat_get, title_entry, x_label_entry, y_label_entry), bg=button_color, font=("Arial", 10, "bold"))
    submit_button.grid(row=6, column=0, columnspan=2, pady=10)




# Bind the choice selection
def choise():
    if clicked.get() == "Bestfit-line":
        bestfit_line()

    elif clicked.get() == "Curve":
         messagebox.showinfo("Curve", "Sorry, not implemented yet!")


choise_button = Button(choise_frame, text="Select", command=choise, bg=button_color, font=("Arial", 10, "bold"))
choise_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()