import tkinter as tk
import psutil

class TaskManager(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Task Manager")
        self.geometry("800x400")

        self.process_list = tk.Listbox(self, width=100)
        self.process_list.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.process_list.bind("<<ListboxSelect>>", self.show_details)

        self.refresh_button = tk.Button(self, text="Refresh", command=self.update_process_list)
        self.refresh_button.pack(pady=5)

        self.details_label = tk.Label(self, text="Process Details:")
        self.details_label.pack(pady=5)

        self.details_text = tk.Text(self, wrap=tk.WORD, height=10, width=100)
        self.details_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.update_process_list()  # Initial process list update

    def update_process_list(self):
        self.process_list.delete(0, tk.END)
        for process in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
            self.process_list.insert(tk.END, f"{process.info['pid']} | {process.info['name']} | {process.info['cpu_percent']}% | {process.info['memory_percent']}%")

    def show_details(self, event):
        selected_index = self.process_list.curselection()
        if selected_index:
            selected_item = self.process_list.get(selected_index)
            pid = selected_item.split()[0]
            details = self.get_process_details(int(pid))
            self.details_text.delete("1.0", tk.END)
            self.details_text.insert(tk.END, details)

    def get_process_details(self, pid):
        try:
            process = psutil.Process(pid)
            details = f"Process Name: {process.name()}\n"
            details += f"Process ID (PID): {process.pid}\n"
            details += f"CPU Usage: {process.cpu_percent(interval=0.1)}%\n"
            details += f"Memory Usage: {process.memory_info().rss / (1024 * 1024):.2f} MB\n"
            details += f"Status: {process.status()}\n"
            details += f"Number of Threads: {process.num_threads()}\n"
            details += f"Parent PID: {process.ppid()}\n"
            details += f"Executable Path: {process.exe()}\n"
            return details
        except psutil.NoSuchProcess:
            return "Process not found."
        except psutil.AccessDenied:
            return "Access denied to process details."

if __name__ == "__main__":
    app = TaskManager()
    app.mainloop()
