from funcs import retrieve_mod, parse_mod_file, download_dependencies
from time import sleep

# Functions

def create_error(err, _type, status):
	return f'ERR: [{_type}] = {err} - [{status}]'


# MAIN

mod_names = parse_mod_file('mc_mods.txt')
installs = 0
errors = []
dependencies = set()
rate_limit = 6
game_version = '1.16.5'
err_threshold = 999
strict = True
destination = 'all_mods'

for mod in mod_names:
	if err_threshold < 1:
		print('ERR: Threshold reached, Breaking...')
		break

	res = retrieve_mod(mod, game_version, strict=strict, dest=destination)

	if res['err'] == False:
		installs += 1

		for x in res['others']:
			dependencies.add(x)

	else:
		err_threshold -= 1

		print(create_error(res['info'], res['sign'], res['status']) + '\n')
		
		if(res['sign'] == 'D-F'):
			errors.append({'name': res['fname'], 'id': res['id']}) 

		sleep(rate_limit)
	sleep(rate_limit // 2)

print(f'DONE: ({installs}/{len(mod_names)}) mods installed.')
print(f'DL: Downloading {len(dependencies)} dependencies.' + '\n')

if len(dependencies) > 0:
	download_dependencies(dependencies, game_version, rate_limit, False, destination)

if len(errors) > 0:
	print([x for x in errors])
