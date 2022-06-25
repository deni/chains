import textwrap
import json

def sign(devices):
	return "NZJr7Gs7YWPL3uZw/5GgEw=="

def chain_create():
	# Generate device key pair
	key_private = ""
	key_public = "rPN7a3A7tLTfcCUTg0gTgQ=="

	# Have the user pick an identifier for the device
	device_name = input("Enter device name: ")

	# Create an object for devices and sign it
	devices = {
		device_name: key_public
	}

	# Sign the devices object
	signature = sign(devices)

	# Create an object to cotain this
	object = {
		"devices": devices,
		"supersedes": None,
		"signee": key_public,
		"signature": signature # "NZJr7Gs7YWPL3uZw/5GgEw=="
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

def print_json(object):
	print(json.dumps(object, indent='\t'))


chain = None
saved = True

print("Welcome to chains.")

while True:
	if chain:
		print("Your current chain:")
		print_json(chain)
	else:
		print("No chain is currently loaded.")

	print(
	'''
	You have the following options:
	[2] Start a new chain
	[1] Load an existing chain
	[3] Save current chain to file
	'''
	)

	choice = input("How do you wish to proceed? ")

	if choice == "1":
		chain = chain_load('signatures/1.json')
	elif choice == "2":
		chain = chain_create()

		print("A new chain has been created and loaded.")
	else:
		print("Please make a choice.")
		choose()

choose(chain)
