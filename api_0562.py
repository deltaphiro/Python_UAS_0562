import json
from flask import request
import mysql.connector
from tabulate import tabulate

dB = mysql.connector.connect(
        host ="localhost",
        user ="root",
        passwd ="",
        database ="db_akademik_0562"
)

cur = dB.cursor()

def db_upload():
	res = request.get("https://api.abcfdab.cfd/students")
	parsing =  json.loads(res.text)
	hasil = parsing['data']
	sql = "INSERT INTO tbl_students_0562 (id, nim, nama, jk, jurusan, alamat) VALUES (%s, %s, %s, %s, %s, %s)" 
	for row in hasil:
		data = (row['id'],row['nim'],row['nama'],row['jk'],row['jurusan'],row['alamat'])
		cur.execute(sql,data)
	dB.commit()
	print("Upload Success!\n")

def show_all():
    select = "select * from tbl_students_0562"
    cur.execute(select)
    result = cur.fetchall()
    print(tabulate(result, headers=['No.', 'NIM', 'Nama', 'JK', 'Jurusan', 'Alamat'], tablefmt='grid'))

def show_by_limit():
        lim = int(input("Masukkan limit: "))
        print('')
        select = "select * from tbl_students_0562 limit %s" % lim
        cur.execute(select)
        result = cur.fetchall()
        print(tabulate(result, headers=['No.', 'NIM', 'Nama', 'JK', 'Jurusan', 'Alamat'], tablefmt='grid'))

def show_by_search():
    lim = input("Masukkan NIM: ")
    select = "select * from tbl_students_0562 where nim = '%s';" % lim
    cur.execute(select)
    result = cur.fetchall()
    print(tabulate(result, headers=['No.', 'NIM', 'Nama', 'JK', 'Jurusan', 'Alamat'], tablefmt='grid'))    


def main():
    while True:
        try:
            print("""
    1. Tampilkan semua data
    2. Tampilkan data berdasarkan limit
    3. Cari berdasarkan NIM
    0. Keluar
            """)
            command = int(input("pilih menu >> "))
        except ValueError:
            print("Masukan tidak boleh kosong\n")
            command = ""
            continue
        if  command in range(1,4): 
            if command == 1:
                show_all()
            elif command == 2:
                show_by_limit()
            elif command == 3:
                show_by_search()
        elif command == 0:
            dB.close()
            break
        else:
            print("Fungsi tidak ditemukan")

if __name__ == '__main__':
    # db_upload()
    main()