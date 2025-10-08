"""
Problem: Menyeberangkan 6 binatang di Kutub Selatan
- Induk pinguin (P), anak pinguin (p)
- Induk singa laut (S), anak singa laut (s)
- Induk beruang kutub (B), anak beruang kutub (b)

Constraint:
1. Balok es hanya muat 2 binatang
2. Anak tidak boleh ditinggal dengan induk jenis lain
3. Singa laut (S) harus sampai pertama kali di sisi lain
"""

from collections import deque
from copy import deepcopy

class State:
    def __init__(self, left, right, boat_pos, path=[], first_trip_done=False):
        self.left = set(left)  # Binatang di sisi kiri
        self.right = set(right)  # Binatang di sisi kanan
        self.boat_pos = boat_pos  # 'left' atau 'right'
        self.path = path.copy()  # Riwayat perpindahan
        self.first_trip_done = first_trip_done  # Apakah perjalanan pertama sudah dilakukan
    
    def __eq__(self, other):
        return (self.left == other.left and 
                self.right == other.right and 
                self.boat_pos == other.boat_pos and
                self.first_trip_done == other.first_trip_done)
    
    def __hash__(self):
        return hash((frozenset(self.left), frozenset(self.right), self.boat_pos, self.first_trip_done))
    
    def is_valid(self):
        """Cek apakah state valid (anak tidak sendirian dengan induk lain)"""
        for side in [self.left, self.right]:
            if len(side) == 0:
                continue
            
            # Cek anak pinguin
            if 'p' in side and 'P' not in side:
                # Ada anak pinguin tanpa induknya
                if 'S' in side or 'B' in side:
                    return False
            
            # Cek anak singa laut
            if 's' in side and 'S' not in side:
                # Ada anak singa laut tanpa induknya
                if 'P' in side or 'B' in side:
                    return False
            
            # Cek anak beruang kutub
            if 'b' in side and 'B' not in side:
                # Ada anak beruang kutub tanpa induknya
                if 'P' in side or 'S' in side:
                    return False
        
        return True
    
    def is_goal(self):
        """Cek apakah semua binatang sudah di sisi kanan"""
        return len(self.left) == 0
    
    def get_next_states(self):
        """Generate semua state berikutnya yang mungkin"""
        next_states = []
        
        if self.boat_pos == 'left':
            current_side = self.left
            other_side = self.right
            new_boat_pos = 'right'
        else:
            current_side = self.right
            other_side = self.left
            new_boat_pos = 'left'
        
        animals = list(current_side)
        
        # Coba pindahkan 1 binatang
        for animal in animals:
            new_current = current_side - {animal}
            new_other = other_side | {animal}
            
            # Tentukan apakah perjalanan pertama sudah dilakukan
            new_first_trip = self.first_trip_done or (self.boat_pos == 'left' and new_boat_pos == 'right')
            
            if self.boat_pos == 'left':
                new_state = State(new_current, new_other, new_boat_pos, 
                                self.path + [f"Pindahkan {animal}"], new_first_trip)
            else:
                new_state = State(new_other, new_current, new_boat_pos, 
                                self.path + [f"Kembali {animal}"], new_first_trip)
            
            # Constraint: Perjalanan pertama HARUS membawa S
            if not self.first_trip_done and self.boat_pos == 'left' and new_boat_pos == 'right':
                if animal != 'S':
                    continue
            
            if new_state.is_valid():
                next_states.append(new_state)
        
        # Coba pindahkan 2 binatang
        for i in range(len(animals)):
            for j in range(i + 1, len(animals)):
                animal1, animal2 = animals[i], animals[j]
                new_current = current_side - {animal1, animal2}
                new_other = other_side | {animal1, animal2}
                
                # Tentukan apakah perjalanan pertama sudah dilakukan
                new_first_trip = self.first_trip_done or (self.boat_pos == 'left' and new_boat_pos == 'right')
                
                if self.boat_pos == 'left':
                    new_state = State(new_current, new_other, new_boat_pos, 
                                    self.path + [f"Pindahkan {animal1} dan {animal2}"], new_first_trip)
                else:
                    new_state = State(new_other, new_current, new_boat_pos, 
                                    self.path + [f"Kembali {animal1} dan {animal2}"], new_first_trip)
                
                # Constraint: Perjalanan pertama HARUS membawa S
                if not self.first_trip_done and self.boat_pos == 'left' and new_boat_pos == 'right':
                    if 'S' not in {animal1, animal2}:
                        continue
                
                if new_state.is_valid():
                    next_states.append(new_state)
        
        return next_states

def solve():
    """Gunakan BFS untuk mencari solusi"""
    # Input symbols
    print(" ")
    print("INPUT (Himpunan Simbol Masukan)")
    print(" ")
    print("P = Induk pinguin")
    print("p = anak pinguin")
    print("S = Induk Singa laut")
    print("s = anak singa laut")
    print("B = induk beruang kutub")
    print("b = anak beruang kutub")
    print("Σ = {P, p, S, s, B, b}")
    print()
    
    # State awal: semua di kiri, balok es di kiri
    initial_state = State({'P', 'p', 'S', 's', 'B', 'b'}, set(), 'left')
    
    if not initial_state.is_valid():
        print("State awal tidak valid!")
        return None
    
    # BFS
    queue = deque([initial_state])
    visited = {initial_state}
    
    while queue:
        current_state = queue.popleft()
        
        if current_state.is_goal():
            return current_state.path
        
        for next_state in current_state.get_next_states():
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
    
    return None

def print_solution(solution):
    """Cetak solusi dengan format yang rapi"""
    if solution is None:
        print("Tidak ada solusi yang ditemukan!")
        return
    
    print(" " * 60)
    print("SOLUSI PENYEBERANGAN")
    print(" " * 60)
    print(f"Total langkah: {len(solution)}")
    print()
    
    # State awal
    left = {'P', 'p', 'S', 's', 'B', 'b'}
    right = set()
    boat = 'left'
    
    print("State Awal:")
    print(f"  Gunung Es Kiri : {', '.join(sorted(left))}")
    print(f"  Balok Es      : [Sisi Kiri]")
    print(f"  Gunung Es Kanan: {', '.join(sorted(right)) if right else '(kosong)'}")
    print()
    
    for i, move in enumerate(solution, 1):
        print(f"Langkah {i}: {move}")
        
        # Update state
        if "Pindahkan" in move:
            # Ambil binatang yang dipindahkan
            animals = move.replace("Pindahkan ", "").replace(" dan ", ",").split(",")
            animals = [a.strip() for a in animals]
            
            for animal in animals:
                left.discard(animal)
                right.add(animal)
            boat = 'right'
        else:  # Kembali
            animals = move.replace("Kembali ", "").replace(" dan ", ",").split(",")
            animals = [a.strip() for a in animals]
            
            for animal in animals:
                right.discard(animal)
                left.add(animal)
            boat = 'left'
        
        # Tampilkan state
        print(f"  Gunung Es Kiri : {', '.join(sorted(left)) if left else '(kosong)'}")
        print(f"  Balok Es      : [Sisi {'Kiri' if boat == 'left' else 'Kanan'}]")
        print(f"  Gunung Es Kanan: {', '.join(sorted(right)) if right else '(kosong)'}")
        print()
    
    print(" ")
    print("SEMUA BINATANG BERHASIL MENYEBERANG!")
    print(" ")

if __name__ == "__main__":
    solution = solve()
    print_solution(solution)
