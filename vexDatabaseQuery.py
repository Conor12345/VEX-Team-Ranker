import json
import requests
import xlwt

# types of available data
# get_events
# get_teams
# get_matches
# get_rankings
# get_awards

while True: # allows for repeated use without restarting the program
    datatype = input("Which data type: ")
    query = input("Query: ")
    response = requests.get("https://api.vexdb.io/v1/" + datatype + "?" + query) # send request to the API
    todos = json.loads(response.text) # load results in JSON, python friendly format

    book = xlwt.Workbook() # initiate sheet
    sheet = book.add_sheet('Sheet 1') # create a blank sheet

    if len(todos["result"]) > 1:
        col = 1
        for j in todos["result"][0]: # import column headings using first result in results
            sheet.write(1, col, str(j))
            col += 1

    row = 2
    for i in todos["result"]: # load each result into a row with all the data supplied
        col = 1
        for j in i:
            sheet.write(row, col, i[j])
            col += 1
        row += 1

    book.save('Sample.xls') # save the sheet to a file
    print("\n\n")


