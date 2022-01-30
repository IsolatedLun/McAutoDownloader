import requests
from bs4 import BeautifulSoup
from time import sleep
import os
from db_funcs import store_to_db, create_insert

'''
 Parses a file that contains the mod names, it converts them to make it compatible with
 the curseforge name format.
'''
def parse_mod_file(file_name):
	print('=========\n' + 'Parsing mod names: ' + file_name + '\n=========\n')

	with open(file_name, 'r') as f:
		parsed_mod_names = []
		names = f.read().splitlines()

		for x in names:
			parsed_mod_names.append('-'.join(x.split(' ')).lower())

		return parsed_mod_names


'''
 Retrieves the project id for the mod in order to download it with the curse.nikky 
 api.
'''
def get_project_id(mod_name):
	print('GET project_id: ' + mod_name)

	try:
		req = requests.get(CACHE_URL + CF_URL + mod_name)
	
		if req.status_code == 429:
			raise Exception(429)

		soup = BeautifulSoup(req.text, 'html.parser')
		about_part = soup.find('div', {'class': 'pb-4 border-b border-gray--100'})
		inner_part = about_part.findChild('div', {'class': 'w-full flex justify-between'})
		id = inner_part.findChildren('span')[1].text

	except Exception as e:
		return {'mod': mod_name, 'sign': 'M-N', 'info': f'Couldn\'t find ID for "{mod_name}".'
		, 'status': e, 'err': True}

	return {'id': id, 'err': False}


'''
 Installs the mod using the curse.nikky api.
'''
def install_mod(proj_id, mod_name, mod_version, strict=False, dest='.'):
	try:
		data = requests.get(CAD_URL + str(proj_id)).json()
		file = data['latestFiles'][-1] if not strict else None
		found = True if mod_version == 'latest' else False

		if(mod_version != 'latest'):
			for mod in data['latestFiles']:
				has_version = compate_versions(mod_version, [x for x in mod['gameVersion']]
				, strict)

				if has_version:
					found = True
					file = mod

		if not found:
			print(f'WARN: {mod_version} unavailable for {mod_name}')

			if strict:
				raise Exception('STRICT')

		print(f'DL: ' + file['fileName'])

		file_content = requests.get(file['downloadUrl']).content

		download_to_destination(file_content, file['fileName'], dest)
		store_to_db('mc_mods', mod_name, proj_id)

		dependencies = search_dependencies(file)


		return {'mod': mod_name, 'err': False, 'others': dependencies}

	except Exception as e:
		return {'mod': mod_name, 'sign': 'D-F', 'id': proj_id \
		, 'fname': mod_name, 'info': f'Couldn\'t download "{mod_name}".'
		, 'status': prettify_err(str(e)), 'err': True}


'''
 Simply searches for dependencies of a mod to be downloaded at the end.
'''
def search_dependencies(mod):
	temp = []

	for dependency in mod['dependencies']:
		if dependency['type'] == 3:
			temp.append(dependency['addonId'])
	
	if len(temp) > 0:
		print(f'INF: Found {len(temp)} dependencies.' + '\n------------\n')
	else:
		print()

	return temp


'''
 Downloads the dependencies of the mods.
'''
def download_dependencies(dependencies, game_version, rate=2, strict=False, dest='.'):
	for dependency in dependencies:
		retrieve_mod('dependency', game_version, False, dependency, strict, dest)
		sleep(rate // 2)

	print('DONE: Installed all dependencies')


'''
 Just makes the error more visually 'pleasing'.
'''
def prettify_err(e):
	if len(e) > 20:
		return '| ' + e[0:19] + ' | ...'
	return e


'''
 Compares the mod versions relatively to avoid edge cases.
'''
def compate_versions(mod_version, versions, strict=False):
	version_key = mod_version[2:4]

	for x in versions:
		if x[2:4] == version_key:
			return True
	return False


'''
 Adds the mod to a specified destination, creates a destination if it doesn't exist,
 "." adds the mod in the current directory.
'''
def download_to_destination(file, fname, dest):
	if not os.path.exists(dest) and dest != '.':
		os.makedirs(dest)

	path = os.path.join(dest, fname) if dest != '.' else fname
	with open(path, 'wb') as f:
		f.write(file)


'''
 A wrapper function to ease error and data handling.
'''
def retrieve_mod(mod, version, url_mode=True, addonId=None, strict=False, dest='.'):
	data = get_project_id(mod) if url_mode else install_mod(addonId, mod, version,
		strict, dest)

	if not data['err'] and url_mode:
		return install_mod(data['id'], mod, version, strict, dest)
	else:
		return data


# VARIABLES
CACHE_URL = 'http://webcache.googleusercontent.com/search?q=cache:'
CF_URL = 'www.curseforge.com/minecraft/mc-mods/'
CAD_URL = 'https://curse.nikky.moe/api/addon/'

HEADERS = {
	'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0",
	'referer': 'https://www.google.com/'
}