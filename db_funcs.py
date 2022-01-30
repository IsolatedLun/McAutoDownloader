'''
 Saves the id in order to avoid future 429's from curseforge.
'''
def store_to_db(table, mod_name, id):
		with open('data.txt', 'a') as f:
			f.write(create_insert(table, {'id': id, 'mod_name': mod_name}) + '\n')


def create_insert(table, data):
    keys, values = '', ''
    inserts = len(data) - 1

    for idx, (key, val) in enumerate(data.items()):
        keys += key
        values += f"'{val}'"
        
        if idx < inserts:
            keys += ','
            values += ','
    
    return f'INSERT INTO {table} ({keys}) VALUES ({values}) ON CONFLICT DO NOTHING' + ';'