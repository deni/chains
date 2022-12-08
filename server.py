import os
import chain_tools


def challenge_generate():
	challenge_bytes = os.urandom(32)
	challenge_string = chain_tools.base64_string(challenge_bytes)

	return challenge_string


challenge_server = challenge_generate()

print("Server's challenge part: " + challenge_server)
