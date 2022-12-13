import base64
import json
import time
from cryptography.hazmat.primitives import hashes


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


def is_base64_string(input):
	try:
		decoded = base64.b64decode(input)
		encoded = base64.b64encode(decoded)
	except:
		return False

	output = encoded.decode('utf-8')

	return input == output


def pretty_log(object):
    serialized_pretty = json.dumps(object, indent='\t')
    log(serialized_pretty)


def chain_clean(untrusted_chain):
	def devices_clean(untrusted_devices):
		devices = {}
		for device_key, device_name in untrusted_devices.items():
			if is_base64_string(device_key):
				devices[device_key] = device_name

		return devices

	chain = []

	for untrusted_chainlink in untrusted_chain:
		untrusted_devices = untrusted_chainlink['devices']
		devices = devices_clean(untrusted_devices)

		untrusted_supersedes = untrusted_chainlink['supersedes']
		untrusted_signee = untrusted_chainlink['signee']
		untrusted_signature = untrusted_chainlink['signature']

		if is_base64_string(untrusted_supersedes) or untrusted_supersedes is None:
			supersedes = untrusted_supersedes
		else: return False
		if is_base64_string(untrusted_signee) or untrusted_signee is None:
			signee = untrusted_signee
		else: return False
		if is_base64_string(untrusted_signature) or untrusted_signature is None:
			signature = untrusted_signature
		else: return False

		chainlink = {
			'devices': devices,
			'supersedes': supersedes,
			'signee': signee,
			'signature': signature,
		}

		chain.append(chainlink)

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


def chain_integrity(chain):
	def link_integrity(link, link_hash_claim):
		link_json_canonical = json_serialize_canonical(link)
		link_hash = crypto_hash_human(link_json_canonical)

		if link_hash == link_hash_claim:
			return True
		else: return False


	if chain[0]['supersedes'] is not None:
		return False

	chain_length = len(chain)

	chainlinks_verified = []
	if chain_length > 1:
		for i in range(1, chain_length):
			chainlinks_verified.append(False)

	# Iterate and skip the last element
	for link_index, chainlink in enumerate(chain[0:-1]):
		# Get hash from the next chainlink
		link_hash_claim = chain[link_index + 1]['supersedes']

		if link_integrity(chainlink, link_hash_claim):
			chainlinks_verified[link_index] = True

	# Check if all the links are verified
	for verified in chainlinks_verified:
		if not verified: break
	else: return True

	return False
