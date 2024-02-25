from random import randint
from timeit import repeat

# importing PyQt5 modules. So we can use the GUI functionality of PyQt5.
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel
import sys  # importing the sys module.

# import matplotlib.pyplot as plt. So we can use the plotting functionality of matplotlib.
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # This allows us to display the figure in the GUI by using the canvas.
from matplotlib.figure import Figure  # FigureCanvasQTAgg is the canvas to display the figure.


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
        merge_sort(L, key)
        merge_sort(R, key)

        i = j = k = 0
        while i < len(L) and j < len(R):
            if key(L[i]) < key(R[j]):
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def quick_sort(arr, key=lambda x: x):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if key(x) <= key(pivot)]
        greater = [x for x in arr[1:] if key(x) > key(pivot)]
        return quick_sort(less, key) + [pivot] + quick_sort(greater, key)


# ---------------------- Timing ----------------------
def run_sorting_algorithm(algorithm, array):
    setup_code = f"from __main__ import {algorithm}"
    stmt = f"{algorithm}({array})"
    times = repeat(setup=setup_code, stmt=stmt, repeat=3, number=10)
    return min(times)


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
        self.button.clicked.connect(self.grab_array_size)   # connects the button to a function.
        self.layout.addWidget(self.button)                  # adds the button to the layout 'Window'.

        self.figure = Figure()                              # creates a figure.
        self.canvas = FigureCanvas(self.figure)             # creates a canvas to display the figure.
        self.layout.addWidget(self.canvas)                  # adds the canvas to the layout 'Window'.

        self.setLayout(self.layout)                         # sets the layout of the window.                       

    def grab_array_size(self):                              # function to grab the array size. will also call main function, which will call the sorting algorithms. main function returns the times of the algorithms.
        array_size = int(self.text_box.text())              # gets the text from the text box and converts it to an integer.
        algo_times = main(array_size)                       # calling the main function with the size of the array. Returns the times.

        self.figure.clear()                                 # clears the figure.
        ax = self.figure.add_subplot(111)                   # adds a subplot to the figure.
        ax.bar(algo_times.keys(), algo_times.values())      # creates a bar chart with the times.
        ax.set_xlabel('Algorithm')                          # sets the x-axis label.
        ax.set_ylabel('Time (s)')                           # sets the y-axis label.
        ax.set_title('Algorithm Speeds')                    # sets the title of the chart.

        self.canvas.draw()


# ---------------------- Main ----------------------
def main(array_size):
    # creates a list of random numbers, given the size of the array.
    array_list = [randint(0, 1000) for _ in range(array_size)]

    sorting_algorithms = {
        'Insertion Sort': insertion_sort,
        'Merge Sort': merge_sort,
        'Quick Sort': quick_sort,
    }

    algo_times = {}  # stores the running times of the algorithms.

    for algorithm_name, algorithm_func in sorting_algorithms.items():
        running_time = run_sorting_algorithm(algorithm_func.__name__, array_list.copy())
        algo_times[algorithm_name] = running_time   # adds the time to the dictionary.

    return algo_times                               # returns the dictionary of times.


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
