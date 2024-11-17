import copy
import numpy as np
import os
import csv
import time

# Funcția citeste_fisier citește datele dintr-un fișier și le prelucrează într-o formă corespunzătoare
def citeste_fisier(file_path):
    d, r = None, None  # Declaram variabilele pentru depozite (d) și magazine (r)
    SCj, Dk, Cjk = [], [], []  # Inițializăm listele pentru stocuri, cereri și matricea costurilor
    reading_Cjk = False  # Variabilă pentru a urmări când citim datele pentru matricea Cjk

    # Deschidem fișierul și citim liniile sale
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Parcurgem fiecare linie a fișierului pentru a extrage datele relevante
    for line in lines:
        line = line.strip()  # Eliminăm spațiile de la începutul și sfârșitul liniei

        # Sărim peste comentarii sau linii goale
        if line.startswith("/") or line.startswith("*") or "instance_name" in line or line == "":
            continue
        # Citim valoarea d (numărul de depozite)
        elif line.startswith("d ="):
            d = int(line.split("=")[1].strip().rstrip(";"))
        # Citim valoarea r (numărul de magazine)
        elif line.startswith("r ="):
            r = int(line.split("=")[1].strip().rstrip(";"))
        # Citim lista SCj (capacitatea fiecărui depozit)
        elif line.startswith("SCj = "):
            SCj = [int(num) for num in line.split("=")[1].strip().strip(";").strip("[]").split()]
        # Citim lista Dk (cerințele fiecărui magazin)
        elif line.startswith("Dk ="):
            Dk = [int(num) for num in line.split("=")[1].strip().strip(";").strip("[]").split()]
        # Citim matricea Cjk (costurile de transport între depozite și magazine)
        elif line.startswith("Cjk ="):
            # Începem să citim matricea, sărind peste "Cjk =" din linie
            line = line.split("=")[1].strip().rstrip(";").strip()
            line = line.replace('[', '').replace(']', '')  # Eliminăm parantezele pătrate
            
            # Procesăm fiecare rând din matricea Cjk
            Cjk.append(list(map(int, line.split())))  # Convertim prima linie într-o listă de int-uri
            reading_Cjk = True  # Indică faptul că am început să citim matricea Cjk
        
        # Continuăm să citim rânduri din matricea Cjk
        elif reading_Cjk:
            if ";" in line:  # În cazul în care linia conține un semn de punctuație pentru încheiere (s-ar putea să fie un semicolon)
                reading_Cjk = False  # Oprim citirea matricei Cjk
            line = line.strip().replace('[', '').replace(']', '')  # Curățăm linia
            row = line.strip().replace(';', '')  # Eliminăm semicolonul de la final
            Cjk.append(list(map(int, row.split())))  # Convertim rândul în int-uri și-l adăugăm în matrice

    # Returnăm rezultatele sub formă de dicționar
    results = {
            "d": d,
            "r": r,
            "SCj": SCj,
            "Dk": Dk,
            "Cjk": Cjk
        }
    
    return results

# Algoritmul minimului pe linie
def minim_pe_linie(d, r, SCj, Dk, Cjk, copie_Cjk):
    # Inițializăm matricea soluției de transport cu zero
    solutie_transport = np.zeros((d, r), dtype=int)
    # Parcurgem fiecare depozit (rand)
    for rand in range(d):
        # În timp ce există stocuri disponibile la depozit și există cerere la magazine
        while SCj[rand] > 0 and sum(Dk) > 0:
            # print(f"Processing depozit {rand}: SCj[{rand}] = {SCj[rand]}, sum(Dk) = {sum(Dk)}")
            minim = min(Cjk[rand])  

            # Verificăm dacă toate costurile sunt inf (ceea ce indică faptul că cererea rămasă nu este acoperită de acest depozit)
            if minim == float('inf'):
                break  # Oprim procesarea acestui depozit

            minim_index = Cjk[rand].index(minim)  # Găsim indexul magazinului cu costul minim
            
             # Determinăm cantitatea care va fi transportată (minimul dintre stocul depozitului și cererea magazinului)
            cost = min(SCj[rand], Dk[minim_index])

            # Actualizăm soluția de transport pentru depozitul respectiv și magazinul corespunzător
            solutie_transport[rand][minim_index] = cost

            # Reducem stocul depozitului și cererea magazinului
            SCj[rand] -= cost
            Dk[minim_index] -= cost

            # Dacă cererea unui magazin a fost satisfăcută, îl excludem din procesare
            if Dk[minim_index] == 0:
                # Setăm costul pe această rută la un număr mare pentru a evita reutilizarea acesteia
                Cjk[rand][minim_index] = float('inf')

    total_cost = 0
    for i in range(d):
        for j in range(r):
            if (solutie_transport[i][j]):
                total_cost += solutie_transport[i][j] * copie_Cjk[i][j]

    # După ce s-au finalizat distribuțiile, afișăm rezultatele
    # print(f"Soluția de transport: \n{solutie_transport}")  # Afișează matricea soluției de transport
    # print(f"Capacitățile rămase în depozite: {SCj}")  # Afișează stocurile rămase
    # rint(f"Cererea rămasă la magazine: {Dk}")  # Afișează cererea rămasă la magazine
    print(f"Costul total este: {total_cost}") # Afișează costul total

    return total_cost

''' -- Citire manuală --
# Citim datele din fișierul specificat
file_path = "./Lab_simple_instances/Lab01_simple_large_01.dat"
rezultat = citeste_fisier(file_path)
d = rezultat["d"]
r = rezultat["r"]
SCj = rezultat["SCj"]
Dk = rezultat["Dk"]
Cjk = rezultat["Cjk"]

# Creăm o copie adâncă a matricei Cjk
copie_Cjk = copy.deepcopy(Cjk)
# print(f"copie cjk: {copie_Cjk}")

# Apelăm funcția pentru a calcula soluția minimului pe linie
rezultat = minim_pe_linie(d, r, SCj, Dk, Cjk, copie_Cjk)
rezultat  # Returnăm rezultatul pentru a-l vizualiza
 '''

def proceseaza_fisiere(): # citire automată
    file_paths = []
    for size in ["small", "medium", "large"]:
        for num in range(1, 26):
            file_paths.append(f"./Lab_simple_instances/Lab01_simple_{size}_{num:02d}.dat")
    results = []
    for file_path in file_paths:
        if os.path.exists(file_path):
            print(f"Procesăm fișierul: {file_path}")
            start_time = time.time()
            rezultat = citeste_fisier(file_path)
            d = rezultat["d"]
            r = rezultat["r"]
            SCj = rezultat["SCj"]
            Dk = rezultat["Dk"]
            Cjk = rezultat["Cjk"]
            copie_Cjk = copy.deepcopy(Cjk)
            cost_total = minim_pe_linie(d, r, SCj, Dk, Cjk, copie_Cjk)
            results.append([file_path[23:], cost_total])
            end_time = time.time()
            print(f"Fișierul {file_path} a fost procesat în {end_time - start_time:.2f} secunde.")
    with open('costuri_totale.csv', mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';', lineterminator='\n')
        writer.writerow(["Fisier", "Cost Total"])
        writer.writerows(results)
    print("Procesele s-au finalizat și costurile totale au fost salvate în 'costuri_totale.csv'.")

proceseaza_fisiere()