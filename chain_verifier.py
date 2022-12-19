import chain_tools
import readline
import json


if __name__ == "__main__":
    untrusted_chain_json = input("Please enter chain to verify: ")
    untrusted_chain = json.loads(untrusted_chain_json)

    if chain_tools.chain_verify(untrusted_chain):
        chain_tools.log("Chain was successfully verified.")
    else:
        chain_tools.log("Chain did not pass verification.")
