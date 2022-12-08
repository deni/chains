# Chains 🔗

Chains makes it possible to create cryptographic signatures from any device, and can then be used to verify that the signature is valid on behalf of an individual. In practice, it means that you can sign data cryptographically from your phone, computer, or another device, after which it can be verified that a specific person made the signature no matter which device was used. The secret **key material** is **generated on the individual device** and **never leaves it**. This also makes it possible to store for a device in its secure hardware (Trusted Platform Module, Secure Enclave, or the likes). This is done decentrally, and only requires the user to trust their own personal devices.

### Use-cases

Being able to create signatures like this, enables various important and useful usecases. The most interesting one being various forms of authentication:

* Single Sign-On solution that not requre trusting any organizarion
* Second-fator verification of various sensitive operations (for instance tranferring money or granting permissions)
* Physical access token

### How does it do this?

It does this by creating objects containing a list of which devices (and their corresponding public key) are allowed to perform operation on the individual's behalf:

```json
[
	{
		"devices": {
			"rPN7a3A7tLTfcCUTg0gTgQ==": "12DEC, MacBook Pro, Kikori Sword"
		},
		"supersedes": null,
		"signee": "rPN7a3A7tLTfcCUTg0gTgQ==",
		"signature": "NZJr7Gs7YWPL3uZw/5GgEw=="
	},
	{
		"devices": {
			"rPN7a3A7tLTfcCUTg0gTgQ==": "12DEC, MacBook Pro, Kikori Sword",
			"QZX5chtFtNNtpxdg043JYQ==": "13FEB, iPhone 4S"
		},
		"supersedes": "81afb37606f93ecaeb33",
		"signee": "rPN7a3A7tLTfcCUTg0gTgQ==",
		"signature": "0Vo4nCUgqtwITSaFwgbikA=="
	},
	{
		"devices": {
			"QZX5chtFtNNtpxdg043JYQ==": "13FEB, iPhone 4S",
			"IZe9WeN9XhR2M+ZryeYMIQ==": "13APR, MacBook Pro, Sword of Time"
		},
		"supersedes": "67e9a38756b70adb3fc1",
		"signee": "QZX5chtFtNNtpxdg043JYQ==",
		"signature": "kaT2uQeDt4rKM0DwsracfA=="
	},
	{
		"devices": {
			"IZe9WeN9XhR2M+ZryeYMIQ==": "13APR, MacBook Pro, Sword of Time",
			"YGHnFQenifuq0ZK2yLn68A==": "14AUG, OnePlus One"
		},
		"supersedes": "fee7fc20da5df64b943b",
		"signee": "IZe9WeN9XhR2M+ZryeYMIQ==",
		"signature": "gqt0M0mOmyOY3RiKIqMNSQ=="
	}
]
```

These objects are called chain links and come together to form a chain that describes the current state and history of which devices (and thereby public keys) are and have been allowed to act on behalf of the individual. When a key is used, the chain is followed back to the start, verifying that each addition was valid when it was created, and that the devices described in the last chain link belong to the same individual as the ones described in the first.

## So it's a blockchain?

No. Although similar in some areas, Chains is **not** a blockchain. Although it works with both *blocks* and *chains* it does not have central consensus. There is no mining, so **not** a traditional blockchain.

However, it is somewhere in that neighborhood, and many of the technologies used to make this project possible were in fact developed in relation to Bitcoin. One of these was HD Wallets as introduced in [Bitcoin Improvement Proposal 32](https://en.bitcoin.it/wiki/BIP_0032).

If the goal of this project was to attrach VC money, an argument could be made for this being close enough to a blockchain. However, as the aim is not to make money, I get the benefit of avoiding the stigma by making it clear that this is not your next Hipster NFT Blockchain Crypto wannabe Pyramid Scheme.
