import secrets
import timeit
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048,) #Generates the Private key
public_key = private_key.public_key() #Generates the Public key

def Gen():
    values = [[0 for _ in range(100)] for _ in range(7)]
    for i in range(1,8,1):
        for y in range(100):
            values[i-1][y] = secrets.token_bytes(2**i)
    return values

def Main():
    values = Gen()
    total_time = timeit.default_timer()
    #Encryption
    total_mean_encrypt = [0 for _ in range(7)]
    for i in range(7):
        for x in range(100):
            mean_encrypt = 0
            for y in range(10):
                start = timeit.default_timer()
                ciphertext = public_key.encrypt(

                    values[i][x],

                    padding.OAEP(

                        mgf=padding.MGF1(algorithm=hashes.SHA256()),

                        algorithm=hashes.SHA256(),

                        label=None
                ))
                mean_encrypt += timeit.default_timer() - start
            total_mean_encrypt[i] += mean_encrypt/10
            values[i][x] = ciphertext
    #Decryption
    total_mean_decrypt = [0 for _ in range(7)]
    for i in range(7):
        for x in range(100):
            mean_decrypt = 0
            for y in range(10):
                start = timeit.default_timer()
                plaintext = private_key.decrypt(

                    values[i][x],

                    padding.OAEP(

                        mgf=padding.MGF1(algorithm=hashes.SHA256()),

                        algorithm=hashes.SHA256(),

                        label=None

                    ))
                mean_decrypt += timeit.default_timer() - start
            total_mean_decrypt[i] += mean_decrypt/10
    for y in range(7):#Prints to the stdout the total mean time of encryption for each file size
        total_mean_encrypt[y] = total_mean_encrypt[y]/100
        total_mean_string = "{:.10f}".format(total_mean_encrypt[y])   
        print("Mean time of encryption for 100 different " + str(2**(y+1)) + " bytes files: " + total_mean_string)
    print()
    for y in range(7):#Prints to the stdout the total mean time of decryption for each file size
        total_mean_decrypt[y] = total_mean_decrypt[y]/100
        total_mean_string = "{:.10f}".format(total_mean_decrypt[y])   
        print("Mean time of decryption for 100 different " + str(2**(y+1)) + " bytes files: " + total_mean_string)
    print("Total time elapsed " + str(timeit.default_timer() - total_time))
        
Main()
