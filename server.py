import os
import chain_tools
import base64
import json
# TMP; weird fix for command line input limit
import readline

def challenge_generate_bytes():
	challenge_bytes = os.urandom(32)

	return challenge_bytes


def verify(chain, publickey, challenge, signature):
	return False


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
chain_unchecked = chain_tools.chain_clean(untrusted_chain)

if chain_tools.chain_integrity(chain_unchecked):
	chain = chain_unchecked
	chain_tools.log("Chain passed integrity check!! \o/")
else:
	chain_tools.log("Chain did not pass integrity check.")
	exit()
