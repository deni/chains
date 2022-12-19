import base64
import json
import time
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature


def base64_string(bytes):
	bytes_base64 = base64.b64encode(bytes)
	string = bytes_base64.decode('utf-8')

	return string


def log(text):
    text_base = '{time} | {text}'
    print(text_base.format(
        time = time.strftime( "%H:%M:%S", time.localtime() ),
        text = text,
    ))


def is_base64_string(input, **kwargs):
	allow_none = kwargs.pop('allow_none', False)

	if allow_none and input is None:
		return True

	try:
		decoded = base64.b64decode(input)
		encoded = base64.b64encode(decoded)
	except:
		return False

	output = encoded.decode('utf-8')

	return input == output


def pretty_log(object):
    serialized_pretty = json.dumps(
		object,
		indent='\t',
	)
    log(serialized_pretty)


def clean_chainlink(untrusted_chainlink):
	def devices_clean(untrusted_devices):
		devices = {}
		for device_key, device_name in untrusted_devices.items():
			if is_base64_string(device_key):
				devices[device_key] = device_name
			else: return False

		return devices


	untrusted_devices = untrusted_chainlink['signed']['devices']

	devices = devices_clean(untrusted_devices)
	if not devices:
		return False

	untrusted_supersedes = untrusted_chainlink['signed']['supersedes']
	untrusted_signee = untrusted_chainlink['signee']
	untrusted_signature = untrusted_chainlink['signature']

	if is_base64_string(untrusted_supersedes, allow_none = True):
		supersedes = untrusted_supersedes
	else: return False
	if is_base64_string(untrusted_signee, allow_none = True):
		signee = untrusted_signee
	else: return False
	if is_base64_string(untrusted_signature, allow_none = True):
		signature = untrusted_signature
	else: return False

	chainlink = {
		'signed': {
			'devices': devices,
			'supersedes': supersedes,
		},
		'signee': signee,
		'signature': signature,
	}

	return chainlink


def clean_chain(untrusted_chain):
	chain = []

	for untrusted_chainlink in untrusted_chain:
		chainlink = clean_chainlink(untrusted_chainlink)

		if chainlink:
			chain.append(chainlink)
		else: return False

	return chain


def json_serialize_canonical(object):
	serialized = json.dumps(object,
		sort_keys = True,
		indent = None,
		separators = (',', ':'),
		ensure_ascii = False,
		allow_nan = False,
	)

	return serialized


def crypto_hash(bytes):
	digest = hashes.Hash(hashes.SHA256())
	digest.update(bytes)
	hash = digest.finalize()

	return(hash)


def crypto_hash_human(string):
	bytes = string.encode('utf-8')
	hashed = crypto_hash(bytes)
	hashed_base64 = base64.b64encode(hashed).decode('utf-8')

	return(hashed_base64)


def object_json_canonical_bytes(signing_object):
	signing_string = json_serialize_canonical(signing_object)
	signing_bytes = signing_string.encode('utf-8')

	return signing_bytes


def signature_verify(publickey_string, signature_string, message):
	publickey_binary = base64.b64decode(publickey_string)
	publickey = serialization.load_der_public_key(publickey_binary)

	signature = base64.b64decode(signature_string)

	try:
		publickey.verify(
			signature,
			message,
			padding.PSS(
				mgf=padding.MGF1(hashes.SHA256()),
				salt_length=padding.PSS.MAX_LENGTH
			),
			hashes.SHA256()
		)
		return True
	except InvalidSignature:
		return False


def chainlink_verify(chainlink, chainlink_previous):
	def chainlink_integrity(chainlink, link_hash_claim):
		link_json_canonical = json_serialize_canonical(chainlink)
		link_hash = crypto_hash_human(link_json_canonical)

		if link_hash == link_hash_claim:
			return True
		else:
			log("Claimed: " + link_hash_claim)
			log("Actual:  " + link_hash)
			return False


	# Is the publickey present in the previous chainlink?
	publickey = chainlink['signee']
	if not publickey in chainlink_previous['signed']['devices']:
		log("Signature was not present in ")
		return False

	# Is the signature correct?
	signature = chainlink['signature']
	signing_object = chainlink['signed']
	signing_bytes = object_json_canonical_bytes(signing_object)
	if not signature_verify(publickey, signature, signing_bytes):
		return False

	# Not we are allowed to interact with the signed part of the object
	# Calculate whether the hash from the previous chainlink is correct
	link_hash_claim = chainlink['signed']['supersedes']
	if not chainlink_integrity(chainlink_previous, link_hash_claim):
		return False

	return True


def chain_verify(chain):
	# Make sure that the first chainlink does not reference an earlier one
	if chain[0]['signed']['supersedes'] is not None:
		return False
	if chain[0]['signature'] is not None:
		return False
	if chain[0]['signee'] is not None:
		return False

	# Iterate, skipping the first element, making the counter start there too
	for link_index, chainlink in enumerate(chain[1:], 1):
		chainlink_previous = chain[link_index - 1]
		if not chainlink_verify(chainlink, chainlink_previous):
			return False

	return True


def select(dict_items, message):
	selection_counter = 1
	for key, value in dict_items:
		print("{}: {}".format(selection_counter, key))
		selection_counter += 1

	selection_int = 0
	message_wrong_input = "Please enter a number corresponding to one of the options above."
	while True:
		selection_string = input(message)

		if selection_string.isnumeric():
			selection_int = int(selection_string)
		else:
			log(message_wrong_input)
			continue

		if 0 < selection_int <= len(dict_items):
			break
		else:
			log(message_wrong_input)

	# Return, from the appropriate dictionary item, the corresponding value
	return dict_items[selection_int - 1][1]


def device_add(
    dirty_chainlink_previous,
    device_new_key_public_string,
    device_new_name,
    **kwargs
):
    skip_cleaning = kwargs.pop('skip_cleaning', False)

    if skip_cleaning:
        chainlink = dirty_chainlink_previous
    else:
        chainlink = clean_chainlink(dirty_chainlink_previous)

    # Verify the speficied public key, and add device to chainlink
    if is_base64_string(device_new_key_public_string):
        chainlink['signed']['devices'][device_new_key_public_string] = device_new_name
    else: return False

    return chainlink


def chain_create(device_publickey_string, device_name):
    chainlink = {
    	'signed': {
    		'devices': {},
    		'supersedes': None,
    	},
    	'signature': None,
		'signee': None,
    }

    chainlink = device_add(
        chainlink,
        device_publickey_string,
        device_name,
        skip_cleaning = True,
    )

    chain = [ chainlink ]

    return chain


def key_private_load_file(key_filename):
	with open(key_filename, 'rb') as key_file:
		privatekey = serialization.load_der_private_key(
			key_file.read(),
			password = None,
		)

	return(privatekey)


def get_publickey_base64(privatekey):
	key_public = privatekey.public_key()
	key_public_der = key_public.public_bytes(
		encoding=serialization.Encoding.DER,
		format=serialization.PublicFormat.SubjectPublicKeyInfo,
	)

	key_public_base64 = base64.b64encode(key_public_der).decode('utf-8')

	return(key_public_base64)


def chainlink_sign(privatekey, chainlink):
	def sign_base64(privatekey, message):
		signature = privatekey.sign(
			message,
			padding.PSS(
				mgf=padding.MGF1(hashes.SHA256()),
				salt_length=padding.PSS.MAX_LENGTH
			),
			hashes.SHA256()
		)

		signature_base64 = base64.b64encode(signature).decode('utf-8')

		return(signature_base64)


	signing_object = chainlink['signed']
	signing_bytes = object_json_canonical_bytes(signing_object)

	signature = sign_base64(privatekey, signing_bytes)

	chainlink['signature'] = signature
	chainlink['signee'] = get_publickey_base64(privatekey)

	return chainlink
