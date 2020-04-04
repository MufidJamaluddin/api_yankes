Realtime Bed Monitoring
===
Script untuk memonitor ketersediaan bed di rumah sakit di Indonesia


Requirements
---
- Python 3
- MySQL
- pipenv


Installation
---
- Clone Aplikasi
    `git clone https://github.com/cekdiri/api_yankes.git`
    `cd api_yankes`

- Buat Virtual Environtment
    Install virtual environtment : `python -m pip install virtualenv`
    Buat virtual environtment : `virtualenv env`
    Jalankan virtual environtment : `./env/Scripts/activate`
    Install library aplikasi dalam virtual environtment : `python -m pip install requirements.pip`

- Jika belum punya pipenv, jalankan `pip install pipenv`
- Jalankan `pipenv install`


Usage
---
    Ubah `settings.cfg`. Isikan data config.
    Jalankan flask command `db_migrate` ketika pertama kali run aplikasi.
    Jalankan `flask run` atau `python wsgi.py` untuk menjalankan API servernya.
    Jalankan flask `sync_data` di cron job.
    

