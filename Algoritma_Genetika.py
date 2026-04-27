import random   # untuk bilangan acak
import math     # untuk fungsi matematika

# Parameter Algoritma Genetika
UKURAN_POPULASI = 125         # Jumlah orang dalam populasi
PANJANG_KROMOSOM = 26         # Panjang kromosom
PC = 0.8                      # Probabilitas Crossover
PM = 0.05                     # Probabilitas Mutasi
GENERASI = 50                 # Jumlah generasi

# Batas nilai domain
X_MIN = -10
X_MAX = 10

# def function objektif dan fitness
def function_objektif(x1, x2):
    try:
        matematika = math.sin(x1) * math.cos(x2) * math.tan(x1 + x2) + 0.5 * math.exp(1 - math.sqrt(x2**2)) # Fungsi matematis mencari matematika minimum dari 𝑓(𝑥1,𝑥2) = −(𝑠𝑖𝑛(𝑥1)𝑐𝑜𝑠(𝑥2)tan(𝑥1 + 𝑥2) + 1/2 exp(1-√x2^2)
        return -matematika
    except:
        return float('inf') # jika error maka return infinity
    
def total_fitness(x1, x2):
    nilai_objektif = function_objektif(x1, x2)
    return -nilai_objektif  # karena mencari nilai Minimum maka semakin negatif semakin terpilih oleh operator seleksi

# inisiasi populasi dan decode
def bikin_kromosom(length):
    return [random.randint(0, 1) for _ in range(length)] # Membuat array biner 1 dan 0

def bikin_populasi_awal(UKURAN_POPULASI, PANJANG_KROMOSOM):     # Membuat populasi dengan membuat 125 array individu, dengan tiap array berisi 26 biner acak 0 dan 1.
    return [bikin_kromosom(PANJANG_KROMOSOM) for _ in range(UKURAN_POPULASI)]   

def dekode_kromosom(kromosom):
    half = len(kromosom) // 2  # Harus dibagi 2 karena gennya dibagi x1 dan x2
    gen_x1 = kromosom[:half]
    gen_x2 = kromosom[half:]
    
    # Konversi biner ke desimal
    dec_x1 = sum([bit * (2 ** i) for i, bit in enumerate(reversed(gen_x1))])
    dec_x2 = sum([bit * (2 ** i) for i, bit in enumerate(reversed(gen_x2))])
    
    # Mapping nilai desimal supaya dalam rentang X_MIN hingga X_MAX
    max_dec = (2 ** half) - 1
    x1 = X_MIN + (X_MAX - X_MIN) * (dec_x1 / max_dec)
    x2 = X_MIN + (X_MAX - X_MIN) * (dec_x2 / max_dec)
    
    return x1, x2

# Operator seleksi
def seleksi_kromosom(populasi, fitness, k=3):
    indeks_terpilih = random.sample(range(len(populasi)), k) # mengambil 3 individu secara acak
    indeks_terbaik = indeks_terpilih[0]
    for idx in indeks_terpilih[1:]:                         # mengecek fitness tertinggi dari 3 individu
        if fitness[idx] > fitness[indeks_terbaik]:
            indeks_terbaik = idx
    return populasi[indeks_terbaik]                        # return individu pemenang sebagai orang tua

# Operator crossover 
def crossover(parent1, parent2, pc):
    if random.random() < pc:    # jika lolos Probablilitas crossover
        sisi_potong = random.randint(1, len(parent1) - 1)
        child1 = parent1[:sisi_potong] + parent2[sisi_potong:]
        child2 = parent2[:sisi_potong] + parent1[sisi_potong:]
        return child1, child2
    return parent1[:], parent2[:] # jika tidak crossover maka binernya akan sama dengan parentnya

# Operator mutasi
def mutasi(kromosom, pm):
    mutasi = kromosom[:]
    for i in range(len(kromosom)):
        if random.random() < pm:    # jika lolos probabilitas mutasi
            mutasi[i] = 1 if mutasi[i] == 0 else 0  # ubah bit (biner): Jika 0 jadi 1, jika 1 jadi 0
    return mutasi

# evolusi
def run_algoritma_genetik():
    populasi = bikin_populasi_awal(UKURAN_POPULASI, PANJANG_KROMOSOM)
    
    # Tempat penyimpanan kromosom terbaik dari setiap generasi
    best_kromosom = None
    best_fitness = -float('inf')
    best_x1 = 0
    best_x2 = 0
    best_nilai_objektif = 0
    
    # dekode dan evaluasi fitness seluruh populasi
    for generasi in range(GENERASI):
        fitness = []
        for kromosom in populasi:       # hitung fitness setiap kromosom
            x1, x2 = dekode_kromosom(kromosom)
            fit = total_fitness(x1, x2)
            fitness.append(fit)
            
            # melacak kromosom terbaik, jika ada yang lebih tinggi maka disimpan
            if fit > best_fitness:
                best_fitness = fit
                best_kromosom = kromosom[:]
                best_x1, best_x2 = x1, x2
                best_nilai_objektif = function_objektif(x1, x2)
                
        # tempat untuk populasi baru
        populasi_baru = []
            
        # mengurutkan populasi lalu ambil 2 terbaik untuk masuk ke populasi baru
        urutkan_populasi = [x for _, x in sorted(zip(fitness, populasi), reverse=True)]
        populasi_baru.extend([urutkan_populasi[0][:], urutkan_populasi[1][:]])
        
        # crossover dan mutasi populasi baru hingga jumlahnya kembali ke awal
        while len(populasi_baru) < UKURAN_POPULASI:
            p1 = seleksi_kromosom(populasi, fitness)
            p2 = seleksi_kromosom(populasi, fitness)
            
            c1, c2 = crossover(p1, p2, PC)
            
            # peluang dapat mutasi
            c1 = mutasi(c1, PM)
            c2 = mutasi(c2, PM)
            
            populasi_baru.extend([c1, c2])
        # hapus jika kelebihan populasi
        populasi = populasi_baru[:UKURAN_POPULASI]
        
    # Hasil akhir
    print("== Hasil Akhir ==")
    print(f"Kromosom Terbaik, adalah {best_kromosom}")
    print(f"Nilai x1 Terbaik, adalah {best_x1:.6f}")
    print(f"Nilai x2 Terbaik, adalah {best_x2:.6f}")
    print(f"Nilai Minimum, adalah {best_nilai_objektif:.6f}")
        
if __name__ == "__main__":
    run_algoritma_genetik()
    
    