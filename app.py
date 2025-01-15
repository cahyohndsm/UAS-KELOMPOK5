from flask import Flask, render_template, request, redirect, url_for
from mysql import connector
from mysql.connector import Error

app = Flask(__name__)

# Open connection
try:
    db = connector.connect(
        host= "8-x5v.h.filess.io",
database = "kelompok5_frogguard",
port = "3307",
username = "kelompok5_frogguard",
password = "05f4f0416fe334a7f4bab84373d6c5bf859b6ff0",

    )

    if db.is_connected():
        print('Open connection successful')
except Error as e:
    print(f"Error connecting to MySQL: {e}")

@app.route('/')
def index():
    try:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM penjualan')  # Mengambil semua data dari tabel penjualan
        result = cursor.fetchall()
        cursor.close()
        return render_template('index.html', hasil=result)  # Mengirim data ke template
    except Error as e:
        print(f"Error executing query: {e}")
        return "An error occurred while fetching data.", 500  # Mengembalikan pesan error
    
@app.route('/kontak')
def kontak():
    return render_template('kontak.html')  # Menampilkan halaman kontak

@app.route('/produk')
def produk():
    return render_template('produk.html')  # Menampilkan halaman produk

@app.route('/tambah')
def tambah_data():
    return render_template('tambah.html')  # Menampilkan form untuk menambah data


@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    try:
        nama_barang = request.form['nama_barang'] 
        jumlah = request.form['jumlah']
        harga = request.form['harga']
        cursor = db.cursor()
        cursor.execute('INSERT INTO penjualan (nama_barang, jumlah, harga) VALUES (%s, %s, %s)', (nama_barang, jumlah, harga))
        db.commit()
        cursor.close()  # Menutup cursor setelah operasi
        return redirect(url_for('index'))  # Mengarahkan kembali ke halaman utama
    except Exception as e:
        print(f"Error: {e}")
        return "Terjadi kesalahan saat menambahkan data", 500  # Menangani kesalahan
    
@app.route('/ubah/<int:id>', methods=['GET'])
def ubah_data(id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM penjualan WHERE id=%s', (id,))
    result = cursor.fetchall()
    cursor.close()
    return render_template('ubah.html', hasil=result)  # Menampilkan form untuk mengubah data

@app.route('/proses_ubah/', methods=['POST'])
def proses_ubah():
    id = request.form['id']
    nama_barang = request.form['nama_barang'] 
    jumlah = request.form['jumlah']
    harga = request.form['harga']
    cursor = db.cursor()
    sql = "UPDATE penjualan SET nama_barang=%s, jumlah=%s, harga=%s WHERE id=%s"  # Corrected table name
    value = (nama_barang, jumlah, harga, id)
    cursor.execute(sql, value)
    db.commit()
    cursor.close()  # Menutup cursor setelah operasi
    return redirect(url_for('index'))  # Mengarahkan kembali ke halaman utama

@app.route('/hapus/<int:id>', methods=['GET'])
def hapus_data(id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM penjualan WHERE id=%s', (id,))
    db.commit()
    cursor.close()  # Menutup cursor setelah operasi
    return redirect(url_for('index'))  # Mengarahkan kembali ke halaman utama

if __name__ == '__main__':
    app.run(debug=True)  # Menjalankan aplikasi dalam mode debug