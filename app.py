import tkinter as tk

class TradingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paper Trading Bot")
        self.geometry("600x400")
        
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
        
    def toggle_trading(self):
        if self.start_stop_button["text"] == "Start Trading":
            self.start_stop_button.configure(text="Stop Trading", bg="red")
            # run trading.py
        else:
            self.start_stop_button.configure(text="Start Trading", bg="green")
        
if __name__ == "__main__":
    app = TradingApp()
    app.mainloop()
