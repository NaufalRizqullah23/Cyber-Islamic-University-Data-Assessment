import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_news(url):
    # Mengambil halaman web menggunakan requests
    response = requests.get(url)
    
    # Memeriksa apakah request berhasil
    if response.status_code == 200:
        # Menggunakan BeautifulSoup untuk parsing HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Menemukan elemen HTML yang berisi teks artikel berita
        news_content = soup.find('div', class_='detail-content')  # Gantilah dengan class atau tag yang sesuai pada website target
        
        # Mendapatkan teks dari elemen HTML
        if news_content:
            article_text = news_content.get_text()
            return article_text
        else:
            print(f"Tidak dapat menemukan konten artikel pada {url}.")
            return None
    else:
        print(f"Gagal mengambil halaman web {url}. Kode status:", response.status_code)
        return None

def count_keywords(text, keywords):
    # Membersihkan teks dari karakter non-alfanumerik dan mengubahnya menjadi huruf kecil
    cleaned_text = re.sub(r'\W', ' ', text.lower())
    
    # Menghitung frekuensi kemunculan kata kunci menggunakan regex
    keyword_counts = {keyword: len(re.findall(rf'\b{re.escape(keyword)}\b', cleaned_text)) for keyword in keywords}
    
    # Menyimpan total frekuensi ke dalam satu kolom "frekuensi"
    keyword_counts['Total_Frekuensi'] = sum(keyword_counts.values())
    
    return keyword_counts

# Daftar URL yang ingin Anda scrape
urls = [
    'https://www.tvonenews.com/berita/167364-kementerian-agama-buka-universitas-islam-siber',

]

# Data untuk menyimpan hasil scraping
result_data = []

# Menentukan kata kunci yang ingin dihitung frekuensinya
keywords_to_count = ['cyber islamic university', 'universitas islam siber', 'ciu']

# Melakukan scraping pada setiap URL
for url in urls:
    article_text = scrape_news(url)
    
    if article_text:
        # Menambahkan teks artikel ke dalam data
        data = {
            'URL': url,
            'Article_Text': article_text
        }

        # Menghitung frekuensi kemunculan kata kunci pada teks artikel
        keyword_counts = count_keywords(article_text, keywords_to_count)
        
        # Menambahkan frekuensi ke dalam data
        data.update(keyword_counts)

        # Menambahkan data ke dalam list
        result_data.append(data)

# Menyimpan list ke dalam file JSON
with open('tvone_full.json', 'w') as json_file:
    json.dump(result_data, json_file, indent=4)

print("Dataset disimpan dalam format JSON.")
