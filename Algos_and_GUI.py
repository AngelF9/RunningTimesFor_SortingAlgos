from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QComboBox # importing PyQt5 modules. So we can use the GUI functionality of PyQt5.
from PyQt5.QtCore import QTimer, QTime # This allows us to display the time in the GUI.
from PyQt5.QtGui import QPalette, QColor # This allows us to change the background color of the GUI.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # This allows us to display the figure in the GUI by using the canvas.
from matplotlib.figure import Figure # FigureCanvasQTAgg is the canvas to display the figure.
from random import randint # For generating a random array
import sys # mporting the sys module.



# ---------------------- Algorithms ----------------------
def insertion_sort(arr, key=lambda x: x):
    for i in range(1, len(arr)):
        key_value = arr[i]
        j = i - 1
        while j >= 0 and key(arr[j]) > key_value:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key_value


def merge_sort(arr, key=lambda x: x):
    if len(arr) > 1:
        mid = len(arr) // 2
        L, R = arr[:mid], arr[mid:]
        yield from merge_sort(L, key) 
        yield from merge_sort(R, key)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if key(L[i]) < key(R[j]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            yield arr.copy() # return the current state of the array

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            yield arr.copy() # return the current state of the array

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            yield arr.copy() # return the current state of the array


def quick_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if key(x) <= key(pivot)]
        greater = [x for x in arr[1:] if key(x) > key(pivot)]
        return quick_sort(less, key) + [pivot] + quick_sort(greater, key)



# ---------------------- GUI ----------------------
class MainWindow(QWidget):  # creating a class that inherits from QWidget.
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()                         # creates 'Window' for where GUI will be displayed.

        self.label = QLabel("Enter array size:")            # creates prompt for user to enter array size.
        self.layout.addWidget(self.label)                   # adds the label to the layout 'Window'.

        self.text_box = QLineEdit()                         # creates a text box for user input.
        self.layout.addWidget(self.text_box)                # adds the text box to the layout 'Window'.

        self.button = QPushButton("Sort Array")             # creates a button for user to click to sort array.
        self.button.clicked.connect(self.animate_sort)   # connects the button to a function.
        self.layout.addWidget(self.button)                  # adds the button to the layout 'Window'.

        self.execution_time_label = QLabel("Total Execution Time: ") # creates a label to display the total execution time.
        self.layout.addWidget(self.execution_time_label) # adds the label to the layout 'Window'.

        self.figure = Figure()                              # creates a figure.
        self.canvas = FigureCanvas(self.figure)             # creates a canvas to display the figure.
        self.layout.addWidget(self.canvas)                  # adds the canvas to the layout 'Window'.

        self.setLayout(self.layout)                         # sets the layout of the window.               

        self.array_size = 0
        self.array_list = []
        self.timer = QTimer(self)
        self.start_time = None


# ---------------------- Helper Functions ----------------------
    def generate_random_array(self): # generates a random array
        self.array_size = int(self.text_box.text()) # gets the text from the text box and converts it to an integer
        self.array_list = [randint(0, 50) for _ in range(self.array_size)] # generates a list of random numbers with values between 0 and 50        

    def animate_sort(self): # function to animate the sorting
        self.generate_random_array() # generates a random array

        sorting_algorithms = {
        'Insertion Sort': insertion_sort,
        'Merge Sort': merge_sort,
        'Quick Sort': quick_sort,
    }
    
        algo_name = 'Merge Sort' # gets the name of the sorting algorithm from the combo box
        algorithm_func = sorting_algorithms[algo_name] # gets the function of the sorting algorithm from the dictionary
        generator = algorithm_func(self.array_list.copy(), key=lambda x: x) # creates a generator for the sorting algorithm

        self.figure.clear()                                 # clears the figure.
        ax = self.figure.add_subplot(111)                   # adds a subplot to the figure.
        ax.set_xlabel('Algorithm')                          # sets the x-axis label.
        ax.set_ylabel('Time (s)')                           # sets the y-axis label.
        bars = ax.bar(range(len(self.array_list)), self.array_list, align="edge", width=0.8) # creates a bar chart with the array list as the height of the bars
        ax.set_xlim(0, len(self.array_list)) # sets the x-axis limits
        ax.set_ylim(0, int(1.1 * max(self.array_list))) # sets the y-axis limits
        ax.set_title("Algorithm : " + algo_name ,
                    fontdict={'fontsize': 12, 'fontweight': 'medium', 'color': '#E4365D'}) # sets the title of the chart
        text = ax.text(0.01, 0.95, "", transform=ax.transAxes, color="#E4365D")
        iteration = [0] # stores the number of iterations

        self.start_time = QTime.currentTime()

        def animate(frame):
            for rect, val in zip(bars, frame):
                rect.set_height(val)
            iteration[0] += 1
            text.set_text("iterations : {}".format(iteration[0]))
            self.canvas.draw()

        def execution_time():
            try:
                A = next(generator)
                animate(A)
            except StopIteration:
                self.timer.stop()
                elapsed_time = self.start_time.elapsed() / 1000.0  # Convert to seconds
                self.execution_time_label.setText(f"Total Execution Time: {elapsed_time:.6f} seconds")

        self.timer.timeout.connect(execution_time) # connect the timer to the execution_time function
        self.timer.start(50) # start the timer



# ---------------------- Main ----------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
