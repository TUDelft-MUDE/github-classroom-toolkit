from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.table import Table, TableStyleInfo


def save_dataframe_to_excel_table(df, filename):
    # Create a new Excel workbook
    wb = Workbook()
    ws = wb.active

    # Write DataFrame to the worksheet row by row
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    # Define the range for the table (starting from A1)
    table_range = f"A1:{chr(65 + len(df.columns) - 1)}{len(df) + 1}"

    # Create a table
    table = Table(displayName="Table1", ref=table_range)

    # Add a table style
    style = TableStyleInfo(name="TableStyleMedium9", showFirstColumn=False,
                           showLastColumn=False, showRowStripes=True, showColumnStripes=True)
    table.tableStyleInfo = style

    # Add the table to the worksheet
    ws.add_table(table)

    # Save the workbook
    if '.xlsx' not in str(filename):
        raise ValueError('Filename must end with .xlsx')
    wb.save(filename)
