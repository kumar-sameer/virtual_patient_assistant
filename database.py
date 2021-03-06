import sqlite3
conn = sqlite3.connect('employee.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE employee
             (employee_id text, employee_name text, service_line text, country text, salary real)''')

# Insert a row of data
# c.execute("INSERT INTO employee VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()