import pandas as pd
import xlsxwriter


def xlsx_create(df, df_logic, output_path, output_filename, report_period, extreme_overspeed):
    """Create an Excel file from the DataFrame."""
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name=output_filename, index=False, startrow=3)
        working_sheet = writer.sheets[output_filename]

        # Create colour formats
        yellow_format = writer.book.add_format({'bg_color': 'yellow'})
        orange_format = writer.book.add_format({'bg_color': '#FFC000', 'bold': True})
        emp_format = writer.book.add_format({'bg_color': '#C8E7CA'})
        emp_format_dark = writer.book.add_format({'bg_color': "#C0DBC2"})
        block_formats = [
            writer.book.add_format({'bg_color': "#FFFFFF"}),
            writer.book.add_format({'bg_color': "#E9E9E9"})
        ]
        date_formats = [
            writer.book.add_format({'num_format': 'yyyy-mm-dd hh:mm', 'bg_color': "#FFFFFF"}),
            writer.book.add_format({'num_format': 'yyyy-mm-dd hh:mm','bg_color': "#E9E9E9"})
        ]

        # Add title and report period
        working_sheet.merge_range('A1:C1', 'Canterbury Overspeed Report', orange_format)
        working_sheet.merge_range('A2:C2', str(report_period), orange_format)

        # Overwrite header row with orange format
        for col_num, col_name in enumerate(df.columns):
            working_sheet.write(3, col_num, col_name, orange_format)

        # set column widths based on contents 
        for index, col in enumerate(df):
            column_len = max(df[col].astype(str).map(len).max(), len(col)) + 2
            working_sheet.set_column(index, index, column_len)

        # Apply alternating block colours
        block = 0
        dt_col = df.columns.get_loc("Date/Time")
        emp_col = df.columns.get_loc("Driver")
        last_col = len(df.columns) - 1
        for row_num, (_, row) in enumerate(df_logic.iterrows(), start=4):
            # Change colour only when this row starts a new cluster
            if not row['Consecutive']: # onto next speeding event
                block += 1
            
            b_fmt = block_formats[block % 2]
            d_fmt = date_formats[block % 2]
            
            for col_num, value in enumerate(row[:last_col+1]):
                if col_num == dt_col and pd.notna(value): # if datetime is not null (NaT - not a time)
                    working_sheet.write_datetime(row_num, col_num, value, d_fmt)
                else:
                    if pd.notna(value):
                        if col_num == emp_col and value.isnumeric():
                            if d_fmt == date_formats[0]: # keep with alternating block colours
                                working_sheet.write(row_num, col_num, value, emp_format)
                            else:
                                working_sheet.write(row_num, col_num, value, emp_format_dark)
                        else:
                            working_sheet.write(row_num, col_num, value, b_fmt)

        # Apply yellow cell colour to extreme overspeed events
        overspeed_col = df.columns.get_loc("Overspeed")
        for row_num, value in enumerate(df["Overspeed"], start=4): 
            if value >= extreme_overspeed: # Extreme overspeed event
                working_sheet.write(row_num, overspeed_col, value, yellow_format)