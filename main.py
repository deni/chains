import textwrap
import json
import copy

def sign(devices):
	return('NZJr7Gs7YWPL3uZw/5GgEw==')

def chain_create():
	# Generate device key pair
	key_private = ''
	key_public = 'rPN7a3A7tLTfcCUTg0gTgQ=='

	# Have the user pick an identifier for the device
	device_name = input("Enter a name for this device: ")

	# Create an object for devices and sign it
	devices = {
		key_public: device_name
	}

	# Sign the devices object
	signature = sign(devices)

	# Create an object to cotain this
	object = {
		'devices': devices,
		'supersedes': None,
		'signee': key_public,
		'signature': signature # "NZJr7Gs7YWPL3uZw/5GgEw=="
	}

	# Put it in a list, creating the first link of the chain
	chain = [object]

	return(chain)

def chain_load(file_path):
	with open(file_path, 'r') as file:
		chain_external = json.load(file)

	# TODO: Check integrity of the chain before returning
	chain_integrity = True

	if chain_integrity:
		return(chain_external)
	else:
		return(None)

def json_serialize(object):
	return(json.dumps(object, indent='\t'))

def device_add(chain):
	device_public_key = input("Enter the public key of the device that you wish to add: ")
	device_name = input("What do you wish to call this device? ")

	link = copy.deepcopy(chain[-1])
	link['devices'][device_public_key] = device_name

	chain.append(link)

	return(chain)

def device_remove(chain):
	link = copy.deepcopy(chain[-1])

	options = []

	for device in link['devices']:
		options.append(str(device))
		print("[{}] {}".format(len(options), link['devices'][device]))

	choice = input("Which key do you wish to delete? ")

	del link['devices'][options[int(choice) - 1]]

	chain.append(link)

	return(chain)

chain = None
saved = True

print("Welcome to chains.")

while True:
	if chain:
		print("Your current chain:")
		print(json_serialize(chain))
	else:
		print("No chain is currently loaded.")

	print(
	'''
	You have the following options:
	[1] Start a new chain
	[2] Load an existing chain from file
	[3] Save current chain to file
	[4] Add device
	[5] Remove device
	'''
	)

	choice = input("How do you wish to proceed? ")

	# If no chain
	if choice == "1":
		chain = chain_create()

		print("A new chain has been created and loaded.")
	elif choice == "2":
		chain = chain_load('signatures/1.json')
	elif choice == "3":
		pass
	elif choice == "4":
		chain = device_add(chain)
	elif choice == "5":
		chain = device_remove(chain)
	else:
		print("Please make a choice.")
		choose()

choose(chain)
