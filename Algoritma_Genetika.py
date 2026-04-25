import random
import math

# Diketahui Algoritma Genetika
POPULASI_SIZE = 100           # Jumlah orang dalam populasi
KROMOSOM_LEN = 16            # Panjang kromosom
PC = 0.9                     # Probabilitas Crossover
PM = 0.06                     # Probabilitas Mutasi
GENERATIONS = 50            # Jumlah generasi

# Batas nilai domain
X_MIN = -10
X_MAX = 10

# def function objektif ddan fitness
def function_objektif(x1, x2):
    try:
        term1 = math.sin(x1) * math.cos(x2) * math.tan(x1 + x2)
        term2 = 0.5 * math.exp(1 - math.sqrt(x2**2))
        return -(term1 + term2)
    except:
        return float('inf')
    
def total_fitness(x1, x2):
    obj_val = function_objektif(x1, x2)
    return -obj_val

# inisiasi populasi dan decode
def bikin_kromosom(length):
    return [random.randint(0, 1) for _ in range(length)]

def bikin_populasi_awal(populasi_size, kromosom_len):
    return [bikin_kromosom(kromosom_len) for _ in range(populasi_size)]

def kromosom_decode(kromosom):
    half = len(kromosom) // 2  # Harus dibagi 2 karena gennya dibagi x1 dan x2
    gen_x1 = kromosom[:half]
    gen_x2 = kromosom[half:]
    
    # Konversi biner ke desimal
    dec_x1 = sum([bit * (2 ** i) for i, bit in enumerate(reversed(gen_x1))])
    dec_x2 = sum([bit * (2 ** i) for i, bit in enumerate(reversed(gen_x2))])
    
    # konversi ke decode
    max_dec = (2 ** half) - 1
    x1 = X_MIN + (X_MAX - X_MIN) * (dec_x1 / max_dec)
    x2 = X_MIN + (X_MAX - X_MIN) * (dec_x2 / max_dec)
    
    return x1, x2

# Operator seleksi
def seleksi_kromosom(populasi, fitness, k=3):
    selected_indices = random.sample(range(len(populasi)), k)
    best_idx = selected_indices[0]
    for idx in selected_indices[1:]:
        if fitness[idx] > fitness[best_idx]:
            best_idx = idx
    return populasi[best_idx]

# Operator crossover 
def crossover(parent1, parent2, pc):
    if random.random() < pc:
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1[:], parent2[:]

# Operator mutasi
def mutasi(kromosom, pm):
    mutated = kromosom[:]
    for i in range(len(kromosom)):
        if random.random() < pm:
            mutated[i] = 1 if mutated[i] == 0 else 0
    return mutated

# evolusi
def run_algoritma_genetik():
    populasi = bikin_populasi_awal(POPULASI_SIZE, KROMOSOM_LEN)
    
    best_kromosom = None
    best_fitness = -float('inf')
    best_x1 = 0
    best_x2 = 0
    best_obj_val = 0
    
    # dekode dan evaluasi fitness seluruh populasi
    for generasi in range(GENERATIONS):
        fitness = []
        for kromosom in populasi:
            x1, x2 = kromosom_decode(kromosom)
            fit = total_fitness(x1, x2)
            fitness.append(fit)
            
            # melacak kromosom terbaik
            if fit > best_fitness:
                best_fitness = fit
                best_kromosom = kromosom[:]
                best_x1, best_x2 = x1, x2
                best_obj_val = function_objektif(x1, x2)
                
        # Membangun populasi baru
        populasi_baru = []
            
        # sorted 2 populasi untuk keturunan selanjutnya
        sorted_populasi = [x for _, x in sorted(zip(fitness, populasi), reverse=True)]
        populasi_baru.extend([sorted_populasi[0][:], sorted_populasi[1][:]])
        
        # Mengisi sisa populasi dengan crossover dan mutasi
        while len(populasi_baru) < POPULASI_SIZE:
            p1 = seleksi_kromosom(populasi, fitness)
            p2 = seleksi_kromosom(populasi, fitness)
            
            c1, c2 = crossover(p1, p2, PC)
            
            c1 = mutasi(c1, PM)
            c2 = mutasi(c2, PM)
            
            populasi_baru.extend([c1, c2])
                
        populasi = populasi_baru[:POPULASI_SIZE]
        
    # Hasil akhir
    print("== Hasil Akhir Algoritma Genetika ==")
    print(f"Kromosom Terbaik: {best_kromosom}")
    print(f"Nilai x1 Terbaik: {best_x1:.6f}")
    print(f"Nilai x2 Terbaik: {best_x2:.6f}")
    print(f"Nilai Minimum f(x): {best_obj_val:.6f}")
        
if __name__ == "__main__":
    run_algoritma_genetik()
    
    
    