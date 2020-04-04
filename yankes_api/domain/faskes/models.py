from yankes_api import app, pw, AppDatabase
from datetime import datetime, timedelta

db = AppDatabase.create(app.config)

class BaseModel(pw.Model):
    class Meta:
        database = db

class JenisFaskes(BaseModel):
    title = pw.CharField(max_length=255)

class Province(BaseModel):
    prov_id = pw.IntegerField()
    nama_prov = pw.CharField(max_length=255)

class RumahSakit(BaseModel):
    prov_id = pw.ForeignKeyField(Province, backref='provinsi')
    kode_rs = pw.IntegerField()
    nama_unit = pw.CharField(max_length=255)
    alamat = pw.TextField()
    jenis_faskes = pw.ForeignKeyField(JenisFaskes, backref='jenis')
    lat = pw.CharField(max_length=255)
    lon = pw.CharField(max_length=255)

class Jenis_Ruang(BaseModel):
    title = pw.CharField(max_length=255)

class Kelas_Ruang(BaseModel):
    title = pw.CharField(max_length=255)

class Occupations(BaseModel):
    rumahsakit = pw.ForeignKeyField(RumahSakit)
    jenis_ruang = pw.ForeignKeyField(Jenis_Ruang)
    kelas_ruang = pw.ForeignKeyField(Kelas_Ruang)
    used_lk = pw.IntegerField(default=0)
    uses_pr = pw.IntegerField(default=0)
    used_ttl = pw.IntegerField(default=0)
    vac_lk = pw.IntegerField(default=0)
    vac_pr = pw.IntegerField(default=0)
    vac_ttl  = pw.IntegerField(default=0)
    waiting = pw.IntegerField(default=0)
    last_update = pw.DateTimeField()
    created_at = pw.DateTimeField(default=datetime.utcnow())
