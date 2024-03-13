import secrets
import timeit
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048,) #Generates the Private key
public_key = private_key.public_key() #Generates the Public key

def Gen():
    values = [0 for _ in range(7)]
    for i in range(1,8,1):
        values[i-1] = secrets.token_bytes(2**i)
    return values

def Main():
    values = Gen()
    for i in values:
        list_encrypt = [0 for _ in range(10)]
        mean_encrypt = 0
        for x in range(10):
            start = timeit.default_timer()
            ciphertext = public_key.encrypt(

                i,

                padding.OAEP(

                    mgf=padding.MGF1(algorithm=hashes.SHA256()),

                    algorithm=hashes.SHA256(),

                    label=None
            ))
            list_encrypt[x] = timeit.default_timer() - start
            mean_encrypt += list_encrypt[x]
        mean_encrypt = mean_encrypt/10
        encrypt_string = "{:.10f}".format(mean_encrypt)
        print("Mean time of encryption for 10 instances of a " + str(len(i)) + " bytes file: " + encrypt_string)
        list_decrypt = [0 for _ in range(10)]
        mean_decrypt = 0
        for y in range(10):
            start = timeit.default_timer()
            plaintext = private_key.decrypt(

                ciphertext,

                padding.OAEP(

                    mgf=padding.MGF1(algorithm=hashes.SHA256()),

                    algorithm=hashes.SHA256(),

                    label=None

                ))
            list_decrypt[y] = timeit.default_timer() - start
            mean_decrypt += list_decrypt[y]
        mean_decrypt = mean_decrypt/10
        decrypt_string = "{:.10f}".format(mean_decrypt)
        print("Mean time of decryption for 10 instances of a " + str(len(i)) + " bytes file: " + decrypt_string)
        if(i != plaintext):
            print("error")
            return
        
Main()
