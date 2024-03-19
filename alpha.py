import timeit
import secrets
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import matplotlib.pyplot as plt

MAX = 1000

def Take_imp():
    while(True):
        try:
            ret = int(input('1 for encrypt, 2 for decrypt'))
            return ret
        except ValueError or (ret >= 3):
            continue

def Rlist(): #Creates a list[7][MAX] which contains all test values for the SHA256 randomized MAX times
    lista = [[0 for _ in range(MAX)] for _ in range(7)]
    for i in range(1,8,1):
        for y in range(MAX):
            lista[i-1][y] = secrets.token_bytes(8**i)
    return lista

def Main():
    total_time = timeit.default_timer() #Times the total elapsed time
    key = AESGCM.generate_key(bit_length=256) #Generates a 256byte key
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    #nonce = os.urandom(12)
    #ct = aesgcm.encrypt(nonce, data, aad)
    #aesgcm.decrypt(nonce, ct, aad)
    total_mean_encrypt = [0 for _ in range(7)]#Keeps count of the mean time for each text size
    total_mean_decrypt = [0 for _ in range(7)]#Keeps count of the mean time for each text size
    data_list = Rlist()
    for u in range(7):
        for i in range(MAX):
            aes_mean_time = 0#Mean time of the substeps
            for x in range(10):#Runs the same aes algorithm for each randomized value of a certain size
                start = timeit.default_timer()
                ciphertext = aesgcm.encrypt(nonce, data_list[u][i], None)
                aes_mean_time += timeit.default_timer() - start#Substep mean time calculation
            aes_mean_time = aes_mean_time/10
            total_mean_encrypt[u] += aes_mean_time#Increments the total mean based on the substeps mean time
            data_list[u][i] = ciphertext#updates the data_list to the cipherd text
    for y in range(7):#Prints to the stdout the total mean time for each file size
        total_mean_encrypt[y] = total_mean_encrypt[y]/MAX
        total_mean_string = "{:.10f}".format(total_mean_encrypt[y])   
        print("Mean time for encryption of " + str(MAX) + " different " + str(len(data_list[y][0])) + " bytes files: " + total_mean_string)
    print()
    for u in range(7):
        for i in range(MAX):
            aes_mean_time = 0#Mean time of the substeps
            for x in range(10):#Runs the same aes algorithm for each randomized value of a certain size
                start = timeit.default_timer()
                ciphertext = aesgcm.decrypt(nonce, data_list[u][i], None)
                aes_mean_time += timeit.default_timer() - start#Substep mean time calculation
            aes_mean_time = aes_mean_time/10
            total_mean_decrypt[u] += aes_mean_time#Increments the total mean based on the substeps mean time
    for y in range(7):#Prints to the stdout the total mean time for each file size
        total_mean_decrypt[y] = total_mean_decrypt[y]/MAX
        total_mean_string = "{:.10f}".format(total_mean_decrypt[y])   
        print("Mean time for decryption of " + str(MAX) + " different " + str(len(data_list[y][0])) + " bytes files: " + total_mean_string)
    x = [8,64,512,4096,32768,262144,2097152] #valor pro plot
    imp = Take_imp()
    if(imp == 1):
        plt.plot(x,total_mean_encrypt)
        plt.show()
    elif(imp == 2):
        plt.plot(x, total_mean_decrypt)
        plt.show()
Main()