from itertools import combinations

def input_jadwal_terisi(input_jam, arr_terisi):
    # Memasukkan inputan jadwal ke array
    input_jam = input_jam.split()
    for jam in input_jam:
        arr_terisi.append(int(jam))

def read_list_matkul(file_path):
    # Membaca list pilihan mata kuliah dari file eksternal dan menyimpannya ke list_pilihan
    list_pilihan = []
    current_matkul = None
    current_kelas = None
    current_jadwal = None
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[15:]:
            line = line.strip()
            if not line:
                continue

            if line == '*':
                if current_matkul:
                    list_pilihan.append([current_matkul, current_kelas, current_jadwal[0], current_jadwal[1], current_jadwal[2], current_jadwal[3], current_jadwal[4]])
                current_matkul = None
                current_kelas = None
                current_jadwal = [[], [], [], [], []]

            elif current_matkul is None:
                current_matkul = line
            elif current_kelas is None:
                current_kelas = line
            else:
                hari, jam_awal, jam_akhir = line.split()
                hari_index = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'].index(hari)
                current_jadwal[hari_index].extend(range(int(jam_awal), int(jam_akhir)))
    
    return list_pilihan

def extract_matkul_names(list_pilihan):
    # Mengeluarkan array berisi nama mata kuliah dari list
    matkul_arr = []
    for data in list_pilihan:
        matkul_name = data[0]
        if matkul_name not in matkul_arr:
            matkul_arr.append(matkul_name)
    return matkul_arr

def is_jadwal_terisi(pilihan1, senin_terisi, selasa_terisi, rabu_terisi, kamis_terisi, jumat_terisi):
    # Mengecek apakah jadwal dari suatu pilihan matkul bentrok dengan jadwal yang telah terisi
    is_bentrok = False
    if bool(set(pilihan1[2]) & set(senin_terisi)):
        is_bentrok = True
    if bool(set(pilihan1[3]) & set(selasa_terisi)):
        is_bentrok = True
    if bool(set(pilihan1[4]) & set(rabu_terisi)):
        is_bentrok = True
    if bool(set(pilihan1[5]) & set(kamis_terisi)):
        is_bentrok = True
    if bool(set(pilihan1[6]) & set(jumat_terisi)):
        is_bentrok = True
    return is_bentrok

def is_jadwal_bentrok(pilihan1, pilihan2):
    # Mengecek apakah jadwal dari 2 pilihan matkul bentrok
    is_bentrok = False
    if bool(set(pilihan1[2]) & set(pilihan2[2])):
        is_bentrok = True
    elif bool(set(pilihan1[3]) & set(pilihan2[3])):
        is_bentrok = True
    elif bool(set(pilihan1[4]) & set(pilihan2[4])):
        is_bentrok = True
    elif bool(set(pilihan1[5]) & set(pilihan2[5])):
        is_bentrok = True
    elif bool(set(pilihan1[6]) & set(pilihan2[6])):
        is_bentrok = True
    return is_bentrok

# IMPLEMENTASI GRAF
def graf_matrix_adj(list_pilihan):
    # Membuat graf dengan representasi adjacency matrix
    # Simpul: pilihan mata kuliah
    # Sisi: jika mata kuliah tidak sama dan tidak ada jadwal yang bentrok
    matrix = [[0 for _ in range(len(list_pilihan))] for _ in range(len(list_pilihan))]
    for i in range(len(list_pilihan)):
        for j in range(len(list_pilihan)):
            if is_terhubung(list_pilihan[i], list_pilihan[j]):
                matrix[i][j] = 1
    return matrix

def is_terhubung(pilihan1, pilihan2):
    # Mengecek apakah 2 simpul terhubung
    terhubung = True
    if pilihan1[0] == pilihan2[0]:
        # Mata kuliah sama
        terhubung = False
    elif is_jadwal_bentrok(pilihan1, pilihan2):
        # Ada jadwal yang bentrok
        terhubung = False
    return terhubung

def is_upagraf_lengkap(kombinasi_n_pilihan, matrix):
    # Mengecek apakah upagraf dengan n simpul merupakan graf lengkap atau bukan
    lengkap = True
    for i in range(len(kombinasi_n_pilihan)):
        for j in range(len(kombinasi_n_pilihan)):
            if i != j:
                if matrix[kombinasi_n_pilihan[i]][kombinasi_n_pilihan[j]] == 0:
                    lengkap = False
    return lengkap

def graf_lengkap_n(banyak_simpul, list_pilihan, matrix):
    # Mengembalikan list berisi semua graf lengkap dengan n simpul
    ada_lengkap = False
    list_graf_lengkap = []
    list_index = [i for i in range(len(list_pilihan))]
    kombinasi = list(combinations(list_index, banyak_simpul))
    for kombin in kombinasi:
        if is_upagraf_lengkap(kombin, matrix):
            ada_lengkap = True
            list_graf_lengkap.append(kombin)
    return list_graf_lengkap, ada_lengkap

def graf_lengkap_max(list_pilihan, matrix):
    # Mengembalikan list berisi semua graf lengkap dengan banyak simpul max
    lengkap = False
    n = len(list_pilihan)
    while not lengkap and n > 0:
        list_graf_lengkap, ada_lengkap = graf_lengkap_n(n, list_pilihan, matrix)
        if ada_lengkap:
            lengkap = True
        n -= 1
    return list_graf_lengkap

def list_kemungkinan_jadwal(list_pilihan, matrix):
    # Mengembalikan list semua kemungkinan jadwal
    list_graf_lengkap = graf_lengkap_max(list_pilihan, matrix)
    list_kemungkinan_jadwal = [[list_pilihan[j] for j in i] for i in list_graf_lengkap]
    return list_kemungkinan_jadwal

def print_satu_matkul(matkul):
    # Menampilkan info mata kuliah ke layar
    print("Mata Kuliah:", matkul[0])
    print("Kelas:", matkul[1])
    list_hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
    for i, hari in enumerate(list_hari):
        jadwal_hari = matkul[i + 2]
        if jadwal_hari:
            jam_mulai = min(jadwal_hari)
            jam_selesai = max(jadwal_hari) + 1
            print(f"{hari} {jam_mulai}.00 - {jam_selesai}.00")

def print_satu_matkul_to_string(matkul):
    # Menampilkan info mata kuliah dalam string 
    result = []
    result.append(f"Mata Kuliah: {matkul[0]}")
    result.append(f"Kelas: {matkul[1]}")
    list_hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat']
    for i, hari in enumerate(list_hari):
        jadwal_hari = matkul[i + 2]
        if jadwal_hari:
            jam_mulai = min(jadwal_hari)
            jam_selesai = max(jadwal_hari) + 1
            result.append(f"{hari} {jam_mulai}.00 - {jam_selesai}.00")
    return "\n".join(result)

def print_kemungkinan_jadwal(list_kemungkinan_jadwal, matkul_all):
    # Menampilkan semua kemungkinan jadwal ke layar
    i = 1
    for jadwal in list_kemungkinan_jadwal:
        print("\nKEMUNGKINAN JADWAL", i)
        print()
        # Menampilkan matkul yang harus di-drop
        matkul = extract_matkul_names(jadwal)
        drop = []
        for mk in matkul_all:
            if mk not in matkul:
                drop.append(mk)
        if drop:
            print("Mata Kuliah yang tidak bisa diambil:", end = " ")
            for k, item in enumerate(drop):
                print(item, end = ", " if k < len(drop) - 1 else "\n")
        j = 1
        for matkuls in jadwal:
            print("- MATKUL", j)
            print_satu_matkul(matkuls)
            j += 1
        i += 1 

def simpan_ke_file(list_kemungkinan_jadwal, matkul_all, output_file):
    # Menyimpan kemungkinan jadwal ke file
    with open(output_file, 'w') as file:
        i = 1
        for jadwal in list_kemungkinan_jadwal:
            file.write(f"KEMUNGKINAN JADWAL {i}\n")
            matkul = extract_matkul_names(jadwal)
            drop = []
            for mk in matkul_all:
                if mk not in matkul:
                    drop.append(mk)
            if drop:
                file.write("Mata Kuliah yang tidak bisa diambil: ")
                file.write(", ".join(drop) + "\n")
            j = 1
            for matkuls in jadwal:
                file.write(f"\n- MATKUL {j}\n")
                file.write(print_satu_matkul_to_string(matkuls))
                j += 1
            file.write("\n\n")
            i += 1

def main():
    print("\nSelamat datang di Pengisian FRS Helper!\n")
    
    # Mengisi jadwal yang telah terisi
    print("Masukkan jadwal Anda yang telah terisi dengan dipisahkan spasi")
    print("Contoh: jika Anda telah memiliki kelas pada pukul 14.00-16.00, masukkan 14 15\n")

    senin_terisi = []
    selasa_terisi = []
    rabu_terisi = []
    kamis_terisi = []
    jumat_terisi = []

    input_jam_senin = input("Senin: ")
    input_jadwal_terisi(input_jam_senin, senin_terisi)

    input_jam_selasa = input("Selasa: ")
    input_jadwal_terisi(input_jam_selasa, selasa_terisi)

    input_jam_rabu = input("Rabu: ")
    input_jadwal_terisi(input_jam_rabu, rabu_terisi)

    input_jam_kamis = input("Kamis: ")
    input_jadwal_terisi(input_jam_kamis, kamis_terisi)

    input_jam_jumat = input("Jumat: ")
    input_jadwal_terisi(input_jam_jumat, jumat_terisi)

    print("\n-------------------------------------------------------------------------------")

    # Membuat array list pilihan dan matkul
    list_pilihan_file = 'matkul.txt'
    list_pilihan = read_list_matkul(list_pilihan_file)
    matkul_all = extract_matkul_names(list_pilihan)
    
    # Menghapus pilihan yang jadwalnya bentrok dengan jadwal terisi
    pilihan_terisi = []
    for pilihan in list_pilihan:
        if is_jadwal_terisi(pilihan, senin_terisi, selasa_terisi, rabu_terisi, kamis_terisi, jumat_terisi):
            pilihan_terisi.append(pilihan)
    list_pilihan = [pilihan for pilihan in list_pilihan if pilihan not in pilihan_terisi]

    # Membuat graf dengan representasi adjacency matrix
    matrix = graf_matrix_adj(list_pilihan)

    # Membuat list kemungkinan semua jadwal dan menampilkannya
    kemungkinan_jadwal = list_kemungkinan_jadwal(list_pilihan, matrix)
    if kemungkinan_jadwal:
        print_kemungkinan_jadwal(kemungkinan_jadwal, matkul_all)

        # Simpan list kemungkinan jadwal ke file txt
        output_file = 'hasil.txt'
        pilihan = input("\nApakah Anda ingin menyimpan hasil ke file? (y/n): ").lower()
        if pilihan == 'y':
            simpan_ke_file(kemungkinan_jadwal, matkul_all, output_file)
            print(f"Hasil telah disimpan ke '{output_file}'.")
    else:
        print("Sayang sekali, tidak ada jadwal yang memenuhi T_T")
        print("Coba ambil matkul lain.")

    print("\nTerima kasih telah menggunakan FRS Helper!")
    print("Goodluck dalam pengisian FRS ^_^\n")
    
if __name__ == "__main__":
    main()