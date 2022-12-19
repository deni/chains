import os
import chain_tools
import base64
import json
# TMP; weird fix for command line input limit
import readline


def challenge_generate_bytes():
	challenge_bytes = os.urandom(32)

	return challenge_bytes


if __name__ == "__main__":
    # Server challenge
    challenge_server_bytes = challenge_generate_bytes()
    challenge_server_string = chain_tools.base64_string(challenge_server_bytes)
    chain_tools.log("Server's challenge part: " + challenge_server_string)

    # Client challenge
    untrusted_challenge_client_string = input("Client's challenge part: ")
    challenge_client_bytes = base64.b64decode(untrusted_challenge_client_string)

    # Mutual challenge
    challenge_concat_bytes = challenge_server_bytes + challenge_client_bytes
    challenge_mutual_bytes = chain_tools.crypto_hash(challenge_concat_bytes)
    challenge_mutual_string = chain_tools.base64_string(challenge_mutual_bytes)
    chain_tools.log("Mutually agreed challenge: " + challenge_mutual_string)

    # Chain
    untrusted_chain_json = input("Please enter chain: ")
    untrusted_chain = json.loads(untrusted_chain_json)
    chain_unchecked = chain_tools.clean_chain(untrusted_chain)
	chain = chain_tools.chain_verify(chain_unchecked)

    if chain_tools.chain_verify(chain_unchecked):
    	chain = chain_unchecked
    	chain_tools.log("Chain passed integrity check!! \o/")
    else:
    	chain_tools.log("Chain did not pass integrity check.")
    	exit()

    # Let the user choose which of these to sign with
    devices = chain[-1]['signed']['devices']
    devices_items_switched = []
    for device_key, device_name in devices.items():
    	devices_items_switched.append( (device_name, device_key) )

    publickey = chain_tools.select(
    	devices_items_switched,
    	"Please select a key to sign with: "
    )

    # Signature
    untrusted_response = input("Please enter signature: ")
    if chain_tools.is_base64_string(untrusted_response):
    	response = untrusted_response
    else:
    	chain_tools.log("ERROR: The signature entered does not seem to convert back and forth from the entered base64.")

	# Public key = publickey
	# Challenge = challenge_mutual_bytes
	# Challenge response = response

    chain_tools.log("The program ended!")
