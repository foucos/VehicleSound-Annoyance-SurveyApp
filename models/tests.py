from createSQLtables import SQL_tables
from user import user

u = user()

table = 'user'
fields = ['UserID', 'Fname', 'Lname','email', 'role','UserName','PasswordHash', 'AccessCode', 'Created_Time']

cl = SQL_tables(table, fields)

cl.set_credentials_file('../config.yml')

t = {
    'UserID': 'INT AUTO_INCREMENT PRIMARY KEY',
    'Fname': 'VARCHAR(50)', 
    'Lname': 'VARCHAR(50)',
    'role': 'VARCHAR(50)',
    'email': 'VARCHAR(50)', 
    'UserName': 'VARCHAR(50)',
    'PasswordHash': 'VARCHAR(100)', 
    'AccessCode': 'INT',
    'Created_Time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP'}

cl.set_types(t)
cl.createTableSQL('user')
u.insert()