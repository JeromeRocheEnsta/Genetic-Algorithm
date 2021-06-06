import random

def writeFile(fileName, E):
    file = open(fileName, "w")
    file.write(str(len(E)) + "\n")
    S = str(E)
    E = S[1:len(S)-1]
    file.write(E)
    file.close()

def randEns_v0(N):
    i = 0
    E = []
    pool = zeroEns(3*N)
    zero = zeroEns(N//2)
    while i < N:
        if (len(pool) > 0):
            E.append(pool.pop(random.randint(0, len(pool) - 1)))
        if (len(zero) > 0):
            E.append(zero.pop(random.randint(0, len(zero) - 1)))
        i+=1
        E = list(set(E))
        random.shuffle(E)
    return E

def randEns(N, linf, lsup, dimSolMin):
    i = 0
    E = []
    pool = zeroEnsLim(linf, lsup)
    zero = zeroEns(dimSolMin//2)
    while i < N:
        if (len(pool) > 0):
            E.append(pool.pop(random.randint(0, len(pool) - 1)))
        if (len(zero) > 0):
            E.insert(random.randint(0, len(E)), zero.pop(random.randint(0, len(zero) - 1)))
        i+=1
    E = list(set(E))
    random.shuffle(E)
    return E

def zeroEns(n):
    pos = list(range(n+1))[1:]
    return [-1 * i for i in pos] + pos

def zeroEns2(N):
    i = 1
    E = []
    while i <= N:
        E.append(i)
        E.append(-1 * i)
        i += 1
    return E

def zeroEnsLim(linf, lsup):
    pos = list(range(lsup+1))[1:]
    return [-1 * i for i in range(abs(linf))] + pos

def ensAleat(N, linf, lsup):
    ens = []
    values = zeroEnsLim(linf, lsup)
    E = (abs(linf) + lsup - N ) * [0]
    ones = N * [1]
    i = 0
    while i < N:
        E.insert(random.randint(0, len(E)), ones.pop(random.randint(0, len(ones) - 1)))
        i += 1
    i = 0
    while i < len(E):
        if E[i] == 1:
            ens.insert(random.randint(0, len(ens)),values[i])
        i += 1
    return ens
    
if __name__ == "__main__":
    E = ensAleat(30, -100, 100)
    writeFile("smallRand.txt", E)
    E = ensAleat(1000, -3000, 3000)
    writeFile("mediumRand.txt", E)
    E = ensAleat(10000, -30000, 2000)
    writeFile("largeRand.txt", E)
    E = ensAleat(50000, -100000, 100000)
    writeFile("extraLargeRand.txt", E)
    E = randEns(30, -100, 100, 10)
    writeFile("small.txt", E)
    E = randEns(1000, -3000, 3000, 200)
    writeFile("medium.txt", E)
    E = randEns(10000, -30000, 2000, 700)
    writeFile("large.txt", E)
    E = randEns(100000, -500000, 500000, 20000)
    writeFile("extralarge.txt", E)
