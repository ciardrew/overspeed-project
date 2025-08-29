import csv
import pandas as pd
import report_generator


def open_and_process_csv(file_path, overspeed_limit, consecutive_time_period):
    """
    Opens and processes the CSV file, returning a filtered DataFrame.
    """
    # Defining arrays for data storage
    speeds = []
    thresholds = []
    overspeeds = []
    bands = []
    datetimes = []
    registrations = []
    display_names = []
    drivers = []
    locations = []
    report_period = ""
    
    with open(file_path, mode='r') as file:
        csvreader = csv.reader(file)
        
        #grab report period from the second row
        for row_num, row in enumerate(csvreader):
            if row_num == 1:
                report_period = row[0]
            elif row_num > 1:
                break
        
        #reset file pointer to the beginning to read data rows
        file.seek(0)
        csvreader = csv.reader(file)
        
        # Skip header rows
        for _ in range(4):
            next(csvreader)

        #Iterate through rows and collect data for overspeed events
        for row in csvreader:
            speed = int(row[1])
            threshold = int(row[2])
            over_by = speed - threshold
            
            if over_by >= overspeed_limit:
                speeds.append(speed)
                thresholds.append(threshold)
                overspeeds.append(over_by)
                bands.append(row[3])
                datetimes.append(row[4])
                registrations.append(row[5])
                display_names.append(row[6])
                drivers.append(row[7])
                locations.append(row[8])

    # Create DataFrame from the collected data
    df = pd.DataFrame({
        "Speed": speeds,
        "Speed Limit": thresholds,
        "Overspeed": overspeeds,
        "Band": bands,
        "Date/Time": datetimes,
        "Registration": registrations,
        "Display Name": display_names,
        "Driver": drivers,
        "Location": locations
    })
    
    
    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format="%d/%m/%Y %H:%M")
    df = df.sort_values('Date/Time')
    
    # Determine if events are consecutive based on time and vehicle registration
    df['PrevTime'] = df.groupby('Registration')['Date/Time'].shift(1)
    df['NextTime'] = df.groupby('Registration')['Date/Time'].shift(-1)
    df['Consecutive'] = (df['Date/Time'] - df['PrevTime']).dt.total_seconds().abs() <= consecutive_time_period
    df['ConsecutiveNext'] = (df['NextTime'] - df['Date/Time']).dt.total_seconds().abs() <= consecutive_time_period

    # Filter for relevant columns
    df_consecutive = df[df['Consecutive'] | df['ConsecutiveNext']].copy()
    df_relevant_cols = df_consecutive[['Speed', 'Speed Limit', 'Overspeed', 'Band', 'Date/Time', 'Registration', 'Display Name', 'Driver', 'Location']]

    return df_relevant_cols, df_consecutive, report_period

def process_and_generate_report(csv_path, output_path, output_filename, overspeed_limit, consecutive_time_period):
    """
    Main function to process data and call the report generation.
    This is called by the GUI.
    """
    df, df_logic, report_period = open_and_process_csv(csv_path, overspeed_limit, consecutive_time_period)
    complete_path = f"{output_path}/{output_filename}.xlsx"
    
    report_generator.xlsx_create(df, complete_path, output_filename, df_logic, report_period)
    