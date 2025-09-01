import csv
import pandas as pd
import report_generator


def open_and_process_csv(file_path, overspeed_limit, consecutive_time_period):
    """Opens and processes the CSV file, returning a filtered DataFrame"""
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
        
        # grab report period from the second row
        for row_num, row in enumerate(csvreader):
            if row_num == 1:
                report_period = row[0]
            elif row_num > 1:
                break
        
        # reset file pointer to the beginning to read data rows
        file.seek(0)
        csvreader = csv.reader(file)

        for _ in range(4):
            next(csvreader)

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

    #sort by rego and datetime to get consecutive events by the same vehicle
    df_sorted = df.sort_values(['Registration', 'Date/Time'])

    # look at prev event by same rego and check its within specified time period
    df_sorted['PrevTime'] = df_sorted.groupby('Registration')['Date/Time'].shift(1)
    df_sorted['Consecutive'] = (df_sorted['Date/Time'] - df_sorted['PrevTime']).dt.total_seconds().abs() <= consecutive_time_period

    # create block id and sort by it. 
    # df_sorted['Consecutive'] is a series of booleans, where False indicates the start of a block
    # ~ negates the series. The start of a block is now True
    # cumsum() increments by 1 when a True is encountered, thus it counts how many new blocks its come across
    df_sorted['Block_ID'] = (~df_sorted['Consecutive']).cumsum()

    # filter only for consecutive events
    df_consecutive = df_sorted[df_sorted['Consecutive'] | df_sorted['Consecutive'].shift(-1)].copy()
    
    # new series with block id as index
    block_start_times = df_consecutive.groupby('Block_ID')['Date/Time'].first().reset_index()
    block_start_times.rename(columns={'Date/Time': 'BlockStartTime'}, inplace=True)
    
    # join tables on block id
    df_final = pd.merge(df_consecutive, block_start_times, on='Block_ID')

    # sort by blockstarttime first, then rego, then date/time
    df_final = df_final.sort_values(['BlockStartTime', 'Registration', 'Date/Time'])
    df_relevant_cols = df_final[['Speed', 'Speed Limit', 'Overspeed', 'Band', 'Date/Time', 'Registration', 'Display Name', 'Driver', 'Location']]
    
    return df_relevant_cols, df_final, report_period

def process_and_generate_report(csv_path, output_path, output_filename, overspeed_limit, consecutive_time_period, extreme_overspeed):
    """ Main function of data_processor.py. Called by GUI and makes the call to create the report"""
    df, df_logic, report_period = open_and_process_csv(csv_path, overspeed_limit, consecutive_time_period)
    complete_path = f"{output_path}/{output_filename}.xlsx"
    
    report_generator.xlsx_create(df, df_logic, complete_path, output_filename, report_period, extreme_overspeed)
    