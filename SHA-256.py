import timeit
import secrets
from cryptography.hazmat.primitives import hashes

def Rlist(): #Creates a list[7][100] which contains all test values for the SHA256 randomized 100 times
    lista = [[0 for _ in range(100)] for _ in range(7)]
    for i in range(1,8,1):
        for y in range(100):
            lista[i-1][y] = secrets.token_bytes(8**i)
    return lista

def Main():
    print("Show substeps?")
    print("[1]Yes(Note displaying the substeps takes considerably more time due to the print funciton)")
    print("[2]No")
    while(True):
        try:
            imp = int(input())
            break
        except ValueError:
            continue
    total_time = timeit.default_timer() #Times the total elapsed time
    digest = hashes.Hash(hashes.SHA256()) #Creates a SHA-256 hash object
    total_mean = [0 for _ in range(7)]#Keeps count of the mean time for each text size
    data_list = Rlist()
    for u in range(7):
        for i in range(100):
            hash_mean_time = 0#Mean time of the substeps
            for x in range(10):#Runs the same hash algorithm for each randomized value of a certain size
                start = timeit.default_timer()
                digest.update(data_list[u][i])#Calculates the hash
                hash_mean_time += timeit.default_timer() - start#Substep mean time calculation
            hash_mean_time = hash_mean_time/10
            hash_string = "{:.10f}".format(hash_mean_time)
            if(imp == 1):#Displays the substeps mean time
                print("Mean time for 10 instances of a " + str(len(data_list[u][0])) + " bytes file: " + hash_string)
            total_mean[u] += hash_mean_time#Increments the total mean based on the substeps mean time
    for y in range(7):#Prints to the stdout the total mean time for each file size
        total_mean[y] = total_mean[y]/100
        total_mean_string = "{:.10f}".format(total_mean[y])   
        print("Mean time for 100 different " + str(len(data_list[y][0])) + " bytes files: " + total_mean_string)
    print("Total time elapsed " + str(timeit.default_timer() - total_time))
Main()
