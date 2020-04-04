from .models import Province, RumahSakit, Occupations, Kelas_Ruang
from playhouse.shortcuts import model_to_dict, dict_to_model

def get_provinces():
    """
    Mendapatkan data list provinsi
    """
    province = Province.select().dicts()
    return list(province)

def get_hospital_by_prov(idprov):
    """
    Mendapatkan data rumah sakit berdasarkan ID Provinsi
    """
    hospitals = RumahSakit.select().where(RumahSakit.prov_id==idprov).dicts()
    return list(hospitals)

def get_okupansis(idprov):
    """
    Mendapatkan data okupansi
    """
    occupation = Occupations.select().join(RumahSakit).where(RumahSakit.prov_id==idprov)
    occp = [model_to_dict(ocp, recurse=True) for ocp in occupation]
    return list(occp)

def get_isolations():
    """
    Mendapatkan data isolasi
    """
    kelas = Kelas_Ruang.select().where(Kelas_Ruang.title.contains('isolasi'))
    kelasruang = [k.id for k in kelas]
    occupation = Occupations.select().where(Occupations.kelas_ruang.in_(kelasruang))
    isolasi = [model_to_dict(isolasi, recurse=True) for isolasi in occupation]
    return list(isolasi)