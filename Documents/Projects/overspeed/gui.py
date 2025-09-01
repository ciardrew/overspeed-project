import tkinter as tk
from tkinter import filedialog, messagebox
import data_processor

class OverspeedApp:
    def __init__(self, root):
        """Constructor."""
        self.root = root
        root.title("Overspeed Report GUI")
        root.geometry("600x600")

        # Define instance variables for user input
        self.path_to_csv = ''
        self.output_path = ''
        self.output_filename = 'overspeed_report'
        self.overspeed_limit = 40
        self.extreme_overspeed = 50
        self.time_period = 13
        self.create_widgets()

    def create_widgets(self):
        """Creates all additional widgets."""
        # Title Strip
        title_frame = tk.Frame(self.root, bg='#439474', height=60)
        title_frame.pack(fill='x')

        title_label = tk.Label(title_frame, text="Overspeed Report Creation", font=("Arial", 18), bg='#439474', fg='white')
        title_label.pack(side='left', padx=10)

        # Help Button
        title_button_help = tk.Button(title_frame, text="Help", command=self.help_pressed, bg='#439474', fg='white', height=1)
        title_button_help.pack(side='right', padx=5)

        ##################################################

        # Input Frame
        input_frame = tk.Frame(self.root, bg='#F0F0F0', height=50)
        input_frame.pack(fill='x', pady=10)

        input_label = tk.Label(input_frame, text="Select CSV File*:", font=("Arial", 12))
        input_label.pack(side='left', padx=10)

        self.input_field = tk.Label(input_frame, text=self.path_to_csv, bg="#FFFFFF", fg='black', width=50, relief='sunken', anchor='w')
        self.input_field.pack(side='left')

        select_input_button = tk.Button(input_frame, text="Browse Files", command=self.browse_file, bg="#ECECEC", fg='black')
        select_input_button.pack(side='right', padx=13)

        ##################################################

        # Divider line
        divider = tk.Frame(self.root, height=2, bg='#CCCCCC')
        divider.pack(fill='x')

        ##################################################

        # Output Section Frame
        output_section_frame = tk.Frame(self.root, bg='#F0F0F0', height=30)
        output_section_frame.pack(fill='x', pady=10)
        output_section_label = tk.Label(output_section_frame, text="Output Excel File Creation", font=("Arial", 14), bg='#F0F0F0')
        output_section_label.pack(side='left', padx=10)

        # Output Frame
        output_frame = tk.Frame(self.root, bg='#F0F0F0', height=50)
        output_frame.pack(fill='x')

        output_label = tk.Label(output_frame, text="Name the Excel file:", font=("Arial", 12))
        output_label.pack(side='left', padx=10)

        self.output_field = tk.Entry(output_frame, text=self.output_filename, bg="#FFFFFF", fg='black', width=50, relief='sunken')
        self.output_field.insert(0, self.output_filename)  # Set default 
        self.output_field.pack(side='left')
        output_button = tk.Button(output_frame, text="Submit Name", command=self.retrieve_output_filename, bg="#ECECEC", fg='black')
        output_button.pack(side='right', padx=13)

        ##################################################

        # Output filename label
        output_filename_label = tk.Frame(self.root, bg="#F0F0F0", height=30)
        output_filename_label.pack(fill='x', pady=5)

        self.output_label = tk.Label(output_filename_label, text=f"Output file will be saved as: {self.output_filename}.xlsx", bg="#F0F0F0", fg='black')
        self.output_label.pack(side='bottom', pady=5)

        ##################################################

        # Output file path
        output_path_frame = tk.Frame(self.root, bg="#F0F0F0", height=100)
        output_path_frame.pack(fill='x', pady=5)

        output_path_label = tk.Label(output_path_frame, text="Save Location*:", font=("Arial", 12), bg='#F0F0F0')
        output_path_label.pack(side='left', padx=10)

        self.output_path_field = tk.Label(output_path_frame, text=self.output_path, bg="#FFFFFF", fg='black', width=50, relief='sunken', anchor='w')
        self.output_path_field.pack(side='left', padx=11)

        select_dir_button = tk.Button(output_path_frame, text="Select Path", command=self.select_output_directory, bg="#ECECEC", fg='black')
        select_dir_button.pack(side='right', padx=13)

        ##################################################

        # Output filepath label
        output_label2_frame = tk.Frame(self.root, bg="#F0F0F0", height=30)
        output_label2_frame.pack(fill='x', pady=5)

        self.output_label2 = tk.Label(output_label2_frame, text=f"Output file will be saved at: {self.output_path}", bg="#F0F0F0", fg='black')
        self.output_label2.pack(side='bottom')

        ##################################################

        # Divider line
        divider2 = tk.Frame(self.root, height=2, bg='#CCCCCC')
        divider2.pack(fill='x', pady=5)

        ##################################################

        # Filter Section Title
        filter_section_frame = tk.Frame(self.root, bg='#F0F0F0', height=30)
        filter_section_frame.pack(fill='x', pady=10)
        filter_section_label = tk.Label(filter_section_frame, text="Filters", font=("Arial", 14), bg='#F0F0F0')
        filter_section_label.pack(side='left', padx=10)

        ##################################################

        # Filter Overspeed Frame
        filter_os_frame = tk.Frame(self.root, bg='#F0F0F0', height=50)
        filter_os_frame.pack(fill='x')

        filter_os_label = tk.Label(filter_os_frame, text="Overspeed Limit to Check:", font=("Arial", 12), bg='#F0F0F0')
        filter_os_label.pack(side='left', padx=10)

        self.overspeed_limit_entry = tk.Entry(filter_os_frame, bg="#FFFFFF", fg='black', width=10, relief='sunken')
        self.overspeed_limit_entry.insert(0, self.overspeed_limit)  # Default overspeed limit
        self.overspeed_limit_entry.pack(side='left', padx=5)

        filter_os_button = tk.Button(filter_os_frame, text="Submit Limit", command=self.overspeed_limit_change, bg="#ECECEC", fg='black')
        filter_os_button.pack(side='right', padx=13)

        ##################################################
        
        #Frame for overspeed label
        os_label_frame = tk.Frame(self.root, bg="#F0F0F0", height=30)
        os_label_frame.pack(fill='x', pady=5)

        self.filter_label2 = tk.Label(os_label_frame, text=f"Overspeed limit set to: {self.overspeed_limit} km/h", bg="#F0F0F0", fg='black')
        self.filter_label2.pack(side='bottom')

        ##################################################

        #Filter Extreme Overspeed Frame
        filter_eos_frame = tk.Frame(self.root, bg='#F0F0F0', height=50)
        filter_eos_frame.pack(fill='x')

        filter_eos_label = tk.Label(filter_eos_frame, text="Extreme Overspeed Limit:", font=("Arial", 12), bg='#F0F0F0')
        filter_eos_label.pack(side='left', padx=10)

        self.extreme_overspeed_limit_entry = tk.Entry(filter_eos_frame, bg="#FFFFFF", fg='black', width=10, relief='sunken')
        self.extreme_overspeed_limit_entry.insert(0, self.extreme_overspeed)  # Default extreme overspeed limit
        self.extreme_overspeed_limit_entry.pack(side='left', padx=5)

        filter_eos_button = tk.Button(filter_eos_frame, text="Submit Limit", command=self.extreme_overspeed_limit_change, bg="#ECECEC", fg='black')
        filter_eos_button.pack(side='right', padx=13)

        ##################################################

        #Frame for extreme overspeed label
        eos_label_frame = tk.Frame(self.root, bg="#F0F0F0", height=30)
        eos_label_frame.pack(fill='x', pady=5)

        self.filter_label3 = tk.Label(eos_label_frame, text=f"Extreme overspeed limit set to: {self.extreme_overspeed} km/h", bg="#F0F0F0", fg='black')
        self.filter_label3.pack(side='bottom')

        ##################################################

        #Filter Time Period Frame
        filter_time_frame = tk.Frame(self.root, bg='#F0F0F0', height=50)
        filter_time_frame.pack(fill='x')

        filter_time_label = tk.Label(filter_time_frame, text="Time Between Overspeeds:", font=("Arial", 12), bg='#F0F0F0')
        filter_time_label.pack(side='left', padx=10)

        self.time_entry = tk.Entry(filter_time_frame, bg="#FFFFFF", fg='black', width=10, relief='sunken')
        self.time_entry.insert(0, self.time_period)  # Default time period between overspeed events
        self.time_entry.pack(side='left', padx=5)

        seconds_label = tk.Label(filter_time_frame, text="seconds", font=("Arial", 10), bg='#F0F0F0')
        seconds_label.pack(side='left')

        filter_time_button = tk.Button(filter_time_frame, text="Submit Time", command=self.time_change, bg="#ECECEC", fg='black')
        filter_time_button.pack(side='right', padx=13)
        

        ##################################################

        #Frame for time period label
        time_label_frame = tk.Frame(self.root, bg="#F0F0F0", height=30)
        time_label_frame.pack(fill='x', pady=5)

        self.filter_label4 = tk.Label(time_label_frame, text=f"Time period set to: {self.time_period} seconds", bg="#F0F0F0", fg='black')
        self.filter_label4.pack(side='bottom')

        ##################################################

        # Divider line
        divider3 = tk.Frame(self.root, height=2, bg='#CCCCCC')
        divider3.pack(fill='x', pady=10)

        ##################################################

        # Create Report Button 
        create_button_frame = tk.Frame(self.root, bg='#F0F0F0', height=50)
        create_button_frame.pack(fill='x')

        create_report_button = tk.Button(create_button_frame, text="Create Overspeed Report", command=self.create_report_command, bg='#439474', fg='white', font=("Arial", 12))
        create_report_button.pack(side='bottom', pady=20)

    def help_pressed(self):
        """Function to create help button window."""
        help_window = tk.Toplevel(self.root)
        help_window.title("Help Window")
        help_window.geometry("300x250")

        scrollbar = tk.Scrollbar(help_window, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        help_text = tk.Text(help_window, wrap="word", yscrollcommand=scrollbar.set)

        input_text = """You must select a CSV file and specify an output path (save location) for a report to be created. \n \nAn Excel file will be created in the specified output path with the filename you provide.  \
            \n \nIf an Excel file with the same name already exists in the outpath path, it will be overwritten with the new report.\n \nIf you choose to change the filename and/or the overspeed limit, you must click the 'Submit Name' and 'Submit Limit' buttons \
                respectively. \n \n"""
        help_text.insert(tk.END, input_text)
        help_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=help_text.yview)
    
    def browse_file(self):
        """Function to browse and select a CSV file."""
        file_path = tk.filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.path_to_csv = file_path
            print(f"Selected file: {self.path_to_csv}")
            self.input_field.config(text=self.path_to_csv)

    def retrieve_output_filename(self):
        """Function to retrieve the output filename from the input field."""
        self.output_filename = self.output_field.get()
        if self.output_filename:
            print(f"Output filename: {self.output_filename}")
            self.output_label.config(text=f"Output file will be saved as: {self.output_filename}.xlsx")
        else:
            self.output_label.config(text=f"Error: No output filename provided. Resubmit")

    def select_output_directory(self):
        """Selects the output directory."""
        self.output_path = filedialog.askdirectory()
        print(f"Selected directory: {self.output_path}")
        self.output_path_field.config(text=self.output_path)
        self.output_label2.config(text=f"Output file will be saved at: {self.output_path}")

    def overspeed_limit_change(self):
        """Function to retrieve the overspeed limit from the entry field."""
        self.overspeed_limit = self.overspeed_limit_entry.get()
        if self.overspeed_limit:
            print(f"Overspeed limit set to: {self.overspeed_limit}")
            self.filter_label2.config(text=f"Overspeed limit set to: {self.overspeed_limit} km/h")
        else:
            print("No overspeed limit provided.")

    def extreme_overspeed_limit_change(self):
        """Function to retrieve the extreme overspeed limit from the entry field."""
        self.extreme_overspeed = self.extreme_overspeed_limit_entry.get()
        if self.extreme_overspeed:
            print(f"Extreme overspeed limit set to: {self.extreme_overspeed}")
            self.filter_label3.config(text=f"Extreme overspeed limit set to: {self.extreme_overspeed} km/h")
        else:
            print("No extreme overspeed limit provided.")

    def time_change(self):
        """Function to retrieve the time period for consecutive overspeed events from the entry field."""
        self.time_period = self.time_entry.get()
        if self.time_period:
            print(f"Time period set to: {self.time_period}")
            self.filter_label4.config(text=f"Time period set to: {self.time_period} seconds")
        else:
            print("No time period provided.")

    def create_report_command(self):
        """Called when the 'Create Report' button is pressed."""
        if self.path_to_csv and self.output_path:
            data_processor.process_and_generate_report(self.path_to_csv, self.output_path, self.output_filename, int(self.overspeed_limit), int(self.time_period), int(self.extreme_overspeed))
            messagebox.showinfo("Success", "Report created successfully!")
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Please select a CSV file and an output path.")



def run_gui():
    """Function to create and run the main GUI window."""
    root = tk.Tk()
    app = OverspeedApp(root)
    root.mainloop()

