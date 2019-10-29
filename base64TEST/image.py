from base64 import b64encode

path = "estacao.eps"

with open(path, "rb") as image:
    encoded_string = b64encode(image.read())

with open("encoded.txt", 'wb') as result:
    result.write(encoded_string)
