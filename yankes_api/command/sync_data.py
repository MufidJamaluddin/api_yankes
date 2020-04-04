from flask import Flask, render_template, request, jsonify, redirect, make_response
import click
from flask import Flask
from yankes_api import app, AppDatabase
from yankes_api.domain.faskes import JenisFaskes, Province, RumahSakit, Jenis_Ruang, Kelas_Ruang, Occupations

import logging
import json
import random
from datetime import datetime, timedelta
import re
import os
import csv

from selenium.webdriver.chrome import ChromeOptions, Chrome

chrome_options = ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

try:
    browser = Chrome(chrome_options=chrome_options)
except:
    browser = Chrome('chromedriver/chromedriver', options=chrome_options)

@click.command()
def sync_data():
    """
    Menambah data dari daftar rumah sakit yang ada di folder data/faskes_rumahsakit.csv
    """
    #db.connect()

    kode_rs = []
    with open('data/faskes_rumahsakit.csv', 'r')  as fle:
        csv_reader = csv.DictReader(fle)
        for row in csv_reader:
            prov  = Province.select().where(Province.prov_id==row['prov_id'])
            if prov.count() < 1:
                prov = Province.create(prov_id=row['prov_id'], nama_prov=row['nama_prov'])

            jenis = JenisFaskes.select().where(JenisFaskes.title==row['jenis_faskes'])
            if jenis.count() < 1:
                jenis =JenisFaskes.create(title=row['jenis_faskes'])
            rs = RumahSakit.select().where(RumahSakit.kode_rs==row['kode_rs'])
            if rs.count() < 1:
                rs = RumahSakit.create(prov_id=prov, 
                    kode_rs=row['kode_rs'], 
                    nama_unit=row['nama_unit'], 
                    alamat=row['alamat'], 
                    jenis_faskes=jenis,
                    lat = row['lat'],
                    lon = row['lng']
                )
            kode_rs.append(row['kode_rs'])

    for kode in kode_rs:
        
        link = 'http://sirs.yankes.kemkes.go.id/integrasi/data/bed_monitor.php?satker='+str(kode)
        browser.get(link)
        #print(r)
        data = browser.page_source
        soup = BeautifulSoup(data, 'lxml')
        table = soup.find('table', attrs={'class':'tbl-responsive table table-striped table-bordered'})
        rs = RumahSakit.select().where(RumahSakit.kode_rs==kode).get()
        if table is not None:
            res = []
            table_rows = table.find_all('tr')

            num_rows = len(table_rows)
            #print(satker+'-'+nama_rs)
            print('recording '+str(kode)+' '+rs.nama_unit)
            i = 0
            for tr in table_rows:
                _satker = kode
                _ruang = '-'
                _kelas = '-'
                _total_kamar = '0'
                _terisi_lk = '0'
                _terisi_pr = '0'
                _total_terisi = '0'
                _kosong_lk = '0'
                _kosong_pr = '0'
                _total_kosong = '0'
                _waiting_list = '0'
                _last_update = '0'
                

                if i>1 and i<(num_rows-1):
                    
                    td = tr.find_all('td')
                    #print(td)
                    row = [tr.text.strip() for tr in td if tr.text.strip()]
                    #print(row)
                    #print(str(i)+'-'+str(len(row)))
                    if len(row)==12:
                        _temp_ruang = row[1]
                    
                    #print(_temp_ruang)
                    if row:

                        if len(row)==12:
                            _ruang = row[1]
                            _kelas = row[2]
                            _total_kamar = row[3] 
                            _terisi_lk = row[4] 
                            _terisi_pr = row[5]
                            _total_terisi = row[6]
                            _kosong_lk = row[7]
                            _kosong_pr = row[8]
                            _total_kosong = row[9]
                            _waiting_list = row[10]
                            _last_update = row[11]

                        elif len(row)==11:
                            _ruang = _temp_ruang
                            _kelas = row[1] 
                            _total_kamar = row[2] 
                            _terisi_lk = row[3] 
                            _terisi_pr = row[4]
                            _total_terisi = row[5]
                            _kosong_lk = row[6]
                            _kosong_pr = row[7]
                            _total_kosong = row[8]
                            _waiting_list = row[9]
                            _last_update = row[10]
                        elif len(row)==10:
                            _ruang = _temp_ruang
                            if row[0].isnumeric():
                                _kelas = '-'
                            else:
                                _kelas = row[0] 
                            _total_kamar = row[1] 
                            _terisi_lk = row[2] 
                            _terisi_pr = row[3]
                            _total_terisi = row[4]
                            _kosong_lk = row[5]
                            _kosong_pr = row[6]
                            _total_kosong = row[7]
                            _waiting_list = row[8]
                            _last_update = row[9]
                        elif len(row)==9:
                            _ruang = _temp_ruang
                            _kelas = '-'
                            _total_kamar = row[0] 
                            _terisi_lk = row[1] 
                            _terisi_pr = row[2]
                            _total_terisi = row[3]
                            _kosong_lk = row[4]
                            _kosong_pr = row[5]
                            _total_kosong = row[6]
                            _waiting_list = row[7]
                            _last_update = row[8]
                        #print(_waiting_list)

                    if _kosong_lk  == '-':
                        _kosong_lk = 0
                    if _kosong_pr == '-':
                        _kosong_pr = 0
                    if _waiting_list == 'N/A':
                        _waiting_list = 0
                    if int(_total_kamar) > 0:
                        ruang = Jenis_Ruang.select().where(Jenis_Ruang.title==_ruang)
                        if ruang.count() < 1:
                            ruang = Jenis_Ruang.create(title=_ruang)
                        else:
                            ruang = ruang.get()
                        kelas = Kelas_Ruang.select().where(Kelas_Ruang.title==_kelas)
                        if kelas.count() < 1:
                            kelas = Kelas_Ruang.create(title=_kelas)
                        else:
                            kelas = kelas.get()   
                        update = dateparser.parse(_last_update)

                        occupation = Occupations.select().where(Occupations.rumahsakit==rs, 
                            Occupations.jenis_ruang==ruang, Occupations.kelas_ruang==kelas, 
                            Occupations.last_update==update)
                        if occupation.count() < 1:
                            occupation = Occupations.create(
                                rumahsakit=rs,
                                jenis_ruang=ruang,
                                kelas_ruang =kelas,
                                used_lk = _terisi_lk,
                                uses_pr = _terisi_pr,
                                used_ttl = _total_terisi,
                                vac_lk = _kosong_lk,
                                vac_pr = _kosong_pr,
                                vac_ttl  = _total_kosong,
                                waiting = _waiting_list,
                                last_update = update
                            )
                i = i +1

    #db.close()