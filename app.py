import tkinter as tk
import subprocess

class TradingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paper Trading Bot")
        self.geometry("600x400")
        
        # Variables
        self.trading_process = None
        
        self.start_stop_button = tk.Button(self, text="Start Trading", command=self.toggle_trading, bg="green", fg="white", font=("Arial", 12, "bold"))
        self.start_stop_button.pack(pady=10)
        
        self.log_label = tk.Label(self, text="Logs:", font=("Arial", 14, "bold"))
        self.log_label.pack(pady=10)
        
        self.log_text = tk.Text(self, height=10, width=50, font=("Arial", 12))
        self.log_text.pack(pady=5)

        self.stock_label = tk.Label(self, text="Current Stocks:", font=("Arial", 14, "bold"))
        self.stock_label.pack(pady=10)
        
        self.stock_text = tk.Text(self, height=10, width=50, font=("Arial", 12))
        self.stock_text.pack(pady=5)

        self.cash_label = tk.Label(self, text="Cash Graph:", font=("Arial", 14, "bold"))
        self.cash_label.pack(pady=10)
        
        self.cash_canvas = tk.Canvas(self, height=200, width=500, bg="white")
        self.cash_canvas.pack(pady=5)

        self.update_logs()
        self.update_stocks()
        self.update_cash_graph()
        
    def toggle_trading(self):
        if self.start_stop_button["text"] == "Start Trading":
            self.start_stop_button.configure(text="Stop Trading", bg="red")
            self.trading_process = subprocess.Popen(["python", "trading.py"])
        else:
            self.start_stop_button.configure(text="Start Trading", bg="green")
            if self.trading_process is not None:
                self.trading_process.terminate()
                self.trading_process = None

    def update_logs(self):
        with open('log.txt', 'r') as f:
            logs = f.read()
        self.log_text.delete('1.0', tk.END)
        self.log_text.insert(tk.END, logs)
        self.after(1000, self.update_logs)

    def update_stocks(self):
        pass

    def update_cash_graph(self):
        with open('cash.txt', 'r') as f:
            cash_data = f.readlines()
        
        cash_values = [float(cash) for cash in cash_data]
        max_cash = max(cash_values)
        min_cash = min(cash_values)
        cash_range = max_cash - min_cash
        
        self.cash_canvas.delete("all")
        
        for i in range(len(cash_values) - 1):
            x1 = i * 10
            y1 = 200 - ((cash_values[i] - min_cash) / cash_range) * 200
            x2 = (i + 1) * 10
            y2 = 200 - ((cash_values[i + 1] - min_cash) / cash_range) * 200
            
            self.cash_canvas.create_line(x1, y1, x2, y2, fill="blue")
        
        self.after(1000, self.update_cash_graph)
        
if __name__ == "__main__":
    app = TradingApp()
    app.mainloop()
