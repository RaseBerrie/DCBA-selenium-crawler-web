import base64

s = 'aHR0cHM6Ly93YWdsZS5pc3BsdXMuam9pbnMuY29tL2FwcC9pbmRleC5waHA\_bWlkPXdnX3R2Jm9yZGVyX3R5cGU9ZGVzYyZzb3J0X2luZGV4PXJlYWRlZF9jb3VudCZkb2N1bWVudF9zcmw9NTEyOTQ2Mg'

result = base64.b64decode(s.replace("\_", "/") + '====').decode('utf-8')
print(result)