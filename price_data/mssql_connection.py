import pyodbc

server = 'DESKTOP-E68FSUV\SQLEXPRESS'
database = 'fin_prices'
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes')
cur = conn.cursor()
cur.execute('select @@version;')
row = cur.fetchone()
while row: 
    print(row[0])
    row = cursor.fetchone()