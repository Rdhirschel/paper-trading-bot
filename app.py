import tkinter as tk
import subprocess
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TradingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paper Trading Bot")
        self.geometry("800x600")
        self.configure(bg='#F0F8FF')  # Light blue background for a cleaner look

        # Variables
        self.trading_process = None

        # Title and introduction
        self.app_title = tk.Label(self, text="Paper Trading Bot", font=("Arial", 24, "bold"), bg='#F0F8FF', fg='black')
        self.app_title.pack(pady=10)

        self.intro_text = tk.Label(self, text="Simulate trading with real-time stock data.", font=("Arial", 16), bg='#F0F8FF', fg='black')
        self.intro_text.pack(pady=10)

        # Start/Stop Button
        self.start_stop_button = tk.Button(self, text="Start Trading", command=self.toggle_trading, bg="#228B22", fg="white", font=("Arial", 14, "bold"), relief=tk.GROOVE)
        self.start_stop_button.pack(pady=10)

        # Clear Logs Button
        self.clear_logs_button = tk.Button(self, text="Clear Logs", command=self.clear_logs, bg="#B22222", fg="white", font=("Arial", 14, "bold"), relief=tk.GROOVE)
        self.clear_logs_button.pack(pady=10)

        # Clear Cash Graph Button
        self.clear_cash_button = tk.Button(self, text="Clear Cash Graph", command=self.clear_cash_graph, bg="#B22222", fg="white", font=("Arial", 14, "bold"), relief=tk.GROOVE)
        self.clear_cash_button.pack(pady=10)

        # Graph Section
        self.cash_label = tk.Label(self, text="Cash Graph:", font=("Arial", 18, "bold"), bg='#F0F8FF', fg='black')
        self.cash_label.pack(pady=10)

        self.cash_figure = Figure(figsize=(5, 4), dpi=100)
        self.cash_canvas = FigureCanvasTkAgg(self.cash_figure, master=self)
        self.cash_canvas.get_tk_widget().pack()

        self.x_axis_label = tk.Label(self, text="Time (secs)", font=("Arial", 14, "bold"), bg='#F0F8FF', fg='black')
        self.x_axis_label.pack(pady=5)

        # Logs Section
        self.log_label = tk.Label(self, text="Logs:", font=("Arial", 18, "bold"), bg='#F0F8FF', fg='black')
        self.log_label.pack(pady=10)

        self.log_text = tk.Text(self, height=10, width=80, font=("Arial", 12), bg='#F5F5F5', fg='black')  # Light gray background
        self.log_text.pack(pady=5)
        self.log_text.configure(state='disabled')

        self.update_logs()
        self.update_cash_graph()

    def toggle_trading(self):
        if self.start_stop_button["text"] == "Start Trading":
            self.start_stop_button.configure(text="Stop Trading", bg="#B22222")  # Red for stopping action
            self.trading_process = subprocess.Popen(["python", "trading.py"])
        else:
            self.start_stop_button.configure(text="Start Trading", bg="#228B22")  # Green for starting action
            if self.trading_process is not None:
                self.trading_process.terminate()
                self.trading_process = None

    def update_logs(self):
        with open('saves/log.txt', 'r') as f:
            logs = f.read()
        self.log_text.configure(state='normal')
        self.log_text.delete('1.0', tk.END)
        self.log_text.insert(tk.END, logs)
        self.log_text.configure(state='disabled')
        self.after(1000, self.update_logs)

    def update_cash_graph(self):
        try:
            self.cash_figure.clear()
            ax = self.cash_figure.add_subplot(111)
            with open('saves/cash.txt', 'r') as f:
                lines = f.readlines()
                cash_values = [float(line) for line in lines]
            ax.plot(cash_values)
            self.cash_canvas.draw()
            self.after(1000, self.update_cash_graph)
        except FileNotFoundError:
            print("Error: No cash data available")

    def clear_logs(self):
        with open('saves/log.txt', 'w') as f:
            f.write("")
        self.update_logs()

    def clear_cash_graph(self):
        with open('saves/cash.txt', 'w') as f:
            f.write("")
        self.update_cash_graph()

if __name__ == "__main__":
    app = TradingApp()
    app.mainloop()
