from scipy import special
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import operator
import math
from itertools import chain

N = 8*10**4 #número de bits--no caso serão criados 1000000 de bits que serão reagrupados em palavras código de 7 bits

Eb_N0_dB = np.arange(11) #multiple Eb/N0 values

Ec_N0_dB = Eb_N0_dB - 10*math.log(7/4,10) 

h = np.array([[1,0,1],[1,1,1],[1,1,0],[0,1,1]])

ht = np.concatenate((h, np.identity(3)), axis=0)
g = np.concatenate((np.identity(4), h), axis=1)
synRef = np.array([5, 7, 6, 3])
bitIdx = np.array([7, 7, 4, 7, 1, 3, 2])
bitIdx = np.reshape(bitIdx, (7, 1))

c_vec = np.zeros((2**4,7))

for kk in range(2**4):
    m_vec = np.array(list(('{0:04b}'.format(kk)).zfill(4)), dtype=int)
    m_vec = np.reshape(m_vec, (1, 4))
    c_vec[kk] = np.dot(m_vec,g)%2

nErr_hard = np.zeros((len(Eb_N0_dB)))
nErr_soft = np.zeros((len(Eb_N0_dB)))

for yy in range(0,len(Eb_N0_dB)):
        
    #Transmitter
    ip = np.round(np.random.rand(1,N))[0] #generating 0,1 with equal probability

    #Hamming coding (7,4)
    #ipM = np.reshape(ip, (4, int(N/4)))
    ipM = np.reshape(ip, (int(N/4),4)) #building messages
    ipC = np.dot(ipM,g)%2 #building code words
    cip = np.reshape(ipC,(1,int((N/4)*7))) #make bit-a-bit
    
    ########################################
    #interleaved -- lambda = 4
    lbd = 4
    intlvd = np.zeros((1,int((N/4)*7)))
    for i in range(int(ipC.shape[0]/lbd)):
        intlvd[0][0+(7*lbd)*i:(7*lbd)+(7*lbd)*i] = np.array(list(chain.from_iterable(zip(cip[0][0+(7*lbd)*i:7+(7*lbd)*i],cip[0][7+(7*lbd)*i:14+(7*lbd)*i],cip[0][14+(7*lbd)*i:21+(7*lbd)*i],cip[0][21+(7*lbd)*i:(7*lbd)+(7*lbd)*i]))))

    cip_ = intlvd
    ########################################
    
    #Modulation
    s = (2*cip_ - 1)[0] #BPSK modulation 0 -> -1; 1 -> 0
    #Channel - AWGN
    mu, sigma = 0, 1
    n = (1/np.sqrt(2))*(np.random.normal(mu, sigma, (1,cip_.shape[1])) + 1j*np.random.normal(mu, sigma, (1,cip_.shape[1]))) #white gaussian noise, 0dB variance
    #Noise addition
    y = s + (10**(-Ec_N0_dB[yy]/20))*n

    ########################################
    #de-interleaving
    deintlvd = np.zeros((1,int((N/4)*7)))
    for i in range(int(ipC.shape[0]/lbd)):
        deintlvd[0][0+(28*i):28+(28*i)] = np.array(list(zip(*[y[0][idx:idx + 4] for idx in range(0+(28*i), 28+(28*i), 4)]))).flatten()
    y_ = deintlvd
    ########################################
    
    #Receiver
    cipHard = np.real(y_)>0
    cipHard = cipHard.astype(int)

    #Hard decision Hamming decoder
    cipHardM = np.reshape(cipHard, (int(N/4),7))
    syndrome = np.dot(cipHardM,ht)%2
    syndromeDec = np.zeros((len(syndrome),1)) 
    for i in range(len(syndrome)):
        syndromeDec[i] = (syndrome[i][0]*2**2 + syndrome[i][1]*2**1 + syndrome[i][2]*2**0)
    syndromeDec[syndromeDec == 0] = 1
    bitCorrIdx = np.zeros((len(syndromeDec),1))
    for i in range(len(syndromeDec)):
        bitCorrIdx[i] = bitIdx[int(syndromeDec[i])-1]
    bitCorrIdx = np.reshape(np.arange(N/4)*7,(int(N/4),1)) + bitCorrIdx #finding the index in the array
    for i in range(len(bitCorrIdx)):
        cipHard[0][int(bitCorrIdx[i])-1] = not(cipHard[0][int(bitCorrIdx[i])-1]) #correcting bits
    idx = np.kron(np.ones((1,int(N/4))), np.arange(1,5)) + np.kron(np.arange(N/4)*7,np.ones((1,4))) #index of data bits
    ipHat_hard = np.zeros((1,len(idx[0])))
    for i in range(len(idx[0])):
        ipHat_hard[0][i] = int(cipHard[0][int(idx[0][i])-1]) #selecting data bits

    #Soft decision Hamming decoder
    cipSoftM = np.reshape(np.real(y_),(int(N/4),7))
    max_index = np.zeros((1,np.dot(cipSoftM,(2*c_vec.transpose()-1)).shape[0]))
    max_value = np.zeros((1,np.dot(cipSoftM,(2*c_vec.transpose()-1)).shape[0]))
    for i in range((np.dot(cipSoftM,(2*c_vec.transpose()-1)).shape[0])):
        max_index[0][i], max_value[0][i] = max(enumerate(np.dot(cipSoftM,(2*c_vec.transpose()-1))[i]), key=operator.itemgetter(1))
    ipHat_soft = np.zeros((1,len(max_index[0])*4))
    for i in range(int(len(max_index[0]))):
        if i == 0:
            #aux = np.concatenate((np.array(list(('{0:04b}'.format(int(max_index[0][0])-1)).zfill(4)), dtype=int),np.array(list(('{0:04b}'.format(int(max_index[0][1])-1)).zfill(4)), dtype=int)), axis=0)    
            aux = np.concatenate((np.array(list(('{0:04b}'.format(int(max_index[0][0]))).zfill(4)), dtype=int),np.array(list(('{0:04b}'.format(int(max_index[0][1]))).zfill(4)), dtype=int)), axis=0)
        elif i > 1:
            aux = np.concatenate((aux,np.array(list(('{0:04b}'.format(int(float(max_index[0][i])))).zfill(4)), dtype=int)), axis=0)
    ipHat_soft = aux

    #counting the errors
    #nErr_hard = np.zeros((len(Eb_N0_dB)))
    nErr_hard[yy] = len(np.where((ip - ipHat_hard[0]) != 0)[0])
    #nErr_soft = np.zeros((len(Eb_N0_dB)))
    nErr_soft[yy] = len(np.where((ip - ipHat_soft) != 0)[0])
    
theoryBer = 0.5*special.erfc(np.sqrt(10**(Eb_N0_dB/10)))
simBer_hard = nErr_hard/N
simBer_soft = nErr_soft/N

plt.semilogy(Eb_N0_dB, theoryBer,'bo',Eb_N0_dB, theoryBer,'b')
plt.semilogy(Eb_N0_dB, theoryBer,'bo',label='theory - uncoded')
plt.semilogy(Eb_N0_dB, simBer_hard, 'mo',Eb_N0_dB, simBer_hard, 'm')
plt.semilogy(Eb_N0_dB, simBer_hard, 'mo',label="simulation - Hamming 7,4 (hard)")
plt.semilogy(Eb_N0_dB, simBer_soft,'ro',Eb_N0_dB, simBer_soft, 'r')
plt.semilogy(Eb_N0_dB, simBer_soft,'ro',label='simulation - Hamming 7,4 (soft)')
plt.xlabel("Eb/No, dB")
plt.ylabel("Bit Error Rate")

#plt.legend(borderaxespad=0)
plt.legend()

plt.show()
