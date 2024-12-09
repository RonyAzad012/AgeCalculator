import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from tkcalendar import Calendar
import logging
import sys

class AgeCalculator(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('age_calculator.log')
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Configure window
        self.title("Age Calculator")
        self.geometry("600x800")
        self.configure(bg='#2C3E50')
        
        # Create main frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.main_frame.configure(bg='#2C3E50')

        # Header
        self.header = tk.Label(
            self.main_frame,
            text="Age Calculator",
            font=("Helvetica", 28, "bold"),
            bg='#2C3E50',
            fg='#ECF0F1'
        )
        self.header.pack(pady=20)

        # Calendar widget
        self.cal = Calendar(
            self.main_frame,
            selectmode='day',
            year=2000,
            month=1,
            day=1,
            background='#34495E',
            foreground='#ECF0F1',
            selectbackground='#2980B9',
            selectforeground='#ECF0F1'
        )
        self.cal.pack(pady=20)

        # Calculate button styling
        style = ttk.Style()
        style.theme_use('clam')  # Use clam theme for better button styling
        style.configure(
            'Accent.TButton',
            font=('Helvetica', 12, 'bold'),
            background='#2980B9',
            foreground='#ECF0F1'
        )
        style.map('Accent.TButton',
            background=[('active', '#3498DB')],
            foreground=[('active', '#ECF0F1')]
        )
        
        self.calc_button = ttk.Button(
            self.main_frame,
            text="Calculate Age",
            command=self.calculate_age,
            style='Accent.TButton'
        )
        self.calc_button.pack(pady=20)

        # Results frame
        self.results_frame = tk.Frame(self.main_frame)
        self.results_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.results_frame.configure(bg='#34495E')

        # Results labels with professional color scheme
        self.results_labels = []
        colors = ['#E74C3C', '#D35400', '#27AE60', '#2980B9', '#8E44AD', '#2C3E50']
        for i in range(6):
            label = tk.Label(
                self.results_frame,
                text="",
                font=("Helvetica", 14, "bold"),
                bg='#34495E',
                fg=colors[i]
            )
            label.pack(pady=10)
            self.results_labels.append(label)

        # Bind enter key to calculate
        self.bind('<Return>', lambda event: self.calculate_age())
        
        # Initialize update_seconds timer
        self.update_timer = None

    def calculate_age(self):
        try:
            selected_date = datetime.combine(self.cal.selection_get(), datetime.min.time())
            now = datetime.now()
            delta = now - selected_date
            
            if selected_date > now:
                error_msg = "Selected date cannot be in the future"
                self.logger.error(error_msg)
                messagebox.showerror("Error", error_msg)
                return
            
            # Age calculations
            years = now.year - selected_date.year - ((now.month, now.day) < (selected_date.month, selected_date.day))
            months = abs(now.month - selected_date.month)
            days = delta.days
            hours = days * 24
            minutes = hours * 60
            
            # Update results labels
            results = [
                f"Years: {years}",
                f"Months: {months}",
                f"Days: {days}",
                f"Hours: {hours:,}",
                f"Minutes: {minutes:,}"
            ]
            
            self.logger.info(f"Calculated age for date: {selected_date.date()}")
            self.logger.debug(f"Results: {results}")
            
            # Update first 5 labels normally
            for label, text in zip(self.results_labels[:5], results):
                label.configure(text=text)
                self.after(200 * self.results_labels.index(label), 
                          lambda l=label: l.configure(fg=l.cget('fg')))
            
            # Start real-time seconds update
            if self.update_timer:
                self.after_cancel(self.update_timer)
            self.update_seconds(selected_date)

        except (ValueError, AttributeError) as e:
            error_msg = "Invalid date selection"
            self.logger.error(f"{error_msg}: {str(e)}")
            messagebox.showerror("Error", error_msg)
        except Exception as e:
            error_msg = "An unexpected error occurred"
            self.logger.critical(f"{error_msg}: {str(e)}")
            messagebox.showerror("Error", f"{error_msg}. Check logs for details.")

    def update_seconds(self, selected_date):
        now = datetime.now()
        delta = now - selected_date
        seconds = int(delta.total_seconds())
        self.results_labels[5].configure(text=f"Seconds: {seconds:,}")
        self.update_timer = self.after(1000, lambda: self.update_seconds(selected_date))

if __name__ == "__main__":
    try:
        app = AgeCalculator()
        app.mainloop()
    except Exception as e:
        logging.critical(f"Application failed to start: {str(e)}")
        sys.exit(1)
