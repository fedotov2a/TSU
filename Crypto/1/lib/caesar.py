def encrypt(m, key):
	return (m + key) % 256

def decrypt(m, key):
	return (m - key) % 256

def encrypt_data(data, key):
	cypher_data = []
	for m in data:
		cypher_data.append(encrypt(m, key))
	return cypher_data

def decrypt_data(data_c, key):
	data = []
	for c in data_c:
		data.append(decrypt(c, key))
	return data