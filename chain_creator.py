import chain_tools


if __name__ == "__main__":
	key_private = chain_tools.key_private_load_file('key.der')
	key_public = chain_tools.get_publickey_base64(key_private)

	chain_tools.log("Key loaded.")
	device_name = input("Please enter device name: ")

	# Create chain, adding device
	# Skip step to calculate hash from previous link as this does not exist
	# Skip step to sign the link, as there is no previous link to provide authorized devices
	chain = chain_tools.chain_create(key_public, device_name)

	# Add another device
	device_2_name = input("Please enter name for 2nd device: ")
	untrusted_device_2_publickey = input("Please enter public key for 2nd device: ")

	if chain_tools.is_base64_string(untrusted_device_2_publickey):
		device_2_publickey = untrusted_device_2_publickey

	chainlink = chain_tools.device_add(
		chain[0],
		device_2_publickey,
		device_2_name,
	)

	chain.append(chainlink)

	# Calculate the hash from the first chainlink
	chainlink_json_canonical = chain_tools.json_serialize_canonical( chain[0] )
	chainlink_hash = chain_tools.crypto_hash_human(chainlink_json_canonical)

	chain[1]['signed']['supersedes'] = chainlink_hash

	# Sign the chainlink with a key from the first chainlink
	chain[1] = chain_tools.chainlink_sign(key_private, chain[1])

	chain_tools.pretty_log(chain)
