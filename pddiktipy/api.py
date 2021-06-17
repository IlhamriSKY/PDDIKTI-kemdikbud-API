from .helper import helper

class api(object):
    def __init__(self):
        self.verify = False
        self.H = helper()
        self.api_link = self.H.endpoint()
        self.api_version = self.H.withversion()

    # Search
    """
    Get all data
    """
    def search_all(self, keyword):
        endpoint = self.api_link+"hit/"+self.H.parse(keyword)
        return self.H.response(endpoint)

    """
    Get Univ only
    Data [text, Nama PT, NPSN, Singkatan, Alamat, website-link]
    Example a.search_pt('University Name')
    """
    def search_pt(self, keyword):
        endpoint = self.api_link+"hit/"+self.H.parse(keyword)
        return self.H.response(endpoint)['pt']

    """
    Get Dosen only
    Data [text, NIDN, PT, Prodi, website-link]
    Example a.search_dosen('Lecturer Name')
    """
    def search_dosen(self, keyword):
        endpoint = self.api_link+"hit/"+self.H.parse(keyword)
        return self.H.response(endpoint)['dosen']

    """
    Get Prodi only
    Data [text, Nama Prodi, Jenjang Prodi, Nama Lembaga, website-link]
    Example a.search_prodi('Sistem Informasi')
    """
    def search_prodi(self, keyword):
        endpoint = self.api_link+"hit/"+self.H.parse(keyword)
        return self.H.response(endpoint)['prodi']

    """
    Get Mahasiswa only
    Data [text(NIM), PT, Prodi, website-link]
    Example a.search_mahasiswa('Ilham Riski Wibowo')
    """
    def search_mahasiswa(self, keyword):
        endpoint = self.api_link+"hit_mhs/"+self.H.parse(keyword)
        return self.H.response(endpoint)

    """
    Get Data By Category
    Example a.search_by_category('mahasiswa', 'Ilham Riski Wibowo')
    """
    def search_by_category(self, category, keyword):
        if (category == 'mahasiswa'):
            return self.search_mahasiswa(keyword)
        elif (category == 'pt'):
            return self.search_pt(keyword)
        elif (category == 'dosen'):
            return self.search_dosen(keyword)
        elif (category == 'prodi'):
            return self.search_prodi(keyword)
        else:
            return self.search_all(keyword)

    # Specific Search
    """
    Search Univ
    Data [current_page, max_page, pt [akreditasi, bujur, id, jln, jumlah_prodi, lintang, logo, nama, no_tel, npsn, provinsi, rasio, singkatan, website]]
    Example a.specific_search_pt('E5E786FB-B8A7-49E6-BAD8-3D8E8E0A4EBF')
    Keyword obtained from search_univ() data "website-link" decoded using base64 or you can using dump_all_univ() and get_uuid_univ_by_name_v2()
    """
    def specific_search_pt(self, keyword = '', provinsi = '',akreditas = '',jenis = '',status = '',koordinasi = '',tipe = '',page = '0'):
        endpoint = self.api_version+'/search_pt'
        payload = "{\"keyword\":\""+keyword+"\",\"provinsi\":\""+provinsi+"\",\"akreditas\":\""+akreditas+"\",\"jenis\":\""+jenis+"\",\"status\":\""+status+"\",\"koordinasi\":\""+koordinasi+"\",\"tipe\":\""+tipe+"\",\"page\":"+page+"}"
        return self.H.post(endpoint, payload)

    """
    Search Dosen
    Data [id, jenjang, nama, nip, prodi, pt]
    Example a.specific_search_dosen('Lecturer Name', '', 'University Name')
    """
    def specific_search_dosen(self, nama = '', nip = '', pt = '', prodi = ''):
        endpoint = self.api_version+'/search_dosen'
        payload = "{\"nama\":\""+nama+"\",\"nip\":\""+nip+"\",\"pt\":\""+pt+"\",\"prodi\":\""+prodi+"\"}"
        return self.H.post(endpoint, payload)

    """
    Search Prodi
    Data [akreditas, id, jenjang, lembaga, nama]
    keyword DA334EA8-53F9-47D2-A832-8B9A689AAD0E
    Example a.specific_search_prodi('DA334EA8-53F9-47D2-A832-8B9A689AAD0E')
    Prodi obtained from search_prodi() data "website-link" decoded using base64 or you can using dump_all_prodi()
    """
    def specific_search_prodi(self, prodi = '', pt = '', wilayah = '', akreditas = '', jenjang = ''):
        endpoint = self.api_version+'/search_prodi'
        payload = "{\"prodi\":\""+prodi+"\",\"pt\":\""+pt+"\",\"wilayah\":\""+wilayah+"\",\"akreditas\":\""+akreditas+"\",\"jenjang\":\""+jenjang+"\"}"
        return self.H.post(endpoint, payload)

    """
    Search Mahasiswa
    Data [id, nama, nipd, prodi, pt]
    Example a.specific_search_mhs('Ilham Riski Wibowo', '', 'Universitas Katolik Soegijapranata', 'Sistem Informasi')
    """
    def specific_search_mhs(self, nama = '', nipd = '', pt = '', prodi = ''):
        endpoint = self.api_version+'/search_mhs'
        payload = "{\"nama\":\""+nama+"\",\"nipd\":\""+nipd+"\",\"pt\":\""+pt+"\",\"prodi\":\""+prodi+"\"}"
        return self.H.post(endpoint, payload)

    # DUMP
    """
    List all Univ with data
    Data [id_sp, kode_pt, nama_pt]
    Example a.dump_all_univ()
    """
    def dump_all_univ(self):
        endpoint = self.api_link+"loadpt"
        return self.H.response(endpoint)

    """
    List all Provinsi
    Data [id, nama]
    Example a.dump_all_provinsi()
    """
    def dump_all_provinsi(self):
        endpoint = self.api_link+"get_provinsi"
        return self.H.response(endpoint)

    """
    List all Prodi
    Data [id_sms, id_sp, kode_prodi, nama_prodi]
    Example a.dump_all_prodi()
    """
    def dump_all_prodi(self):
        endpoint = self.api_link+"loadprodi"
        return self.H.response(endpoint)

    """
    In Script Search
    Data [id_sp, kode_pt, nama_pt]
    Example a.get_univ_by_name('University Name')
    Don't use this, because search fuction hardcoded on the client side instead of the server
    """
    def get_univ_by_name(self, univ_name):
        endpoint = self.api_link+"loadpt"
        data = self.H.response(endpoint)
        try:
            result = list(filter(lambda x: univ_name.capitalize() in x["nama_pt"],data))
        except KeyError:
            result = "Data doesn't exist"
        return result

    """
    Get id_sp or uuid Univ V1
    Example a.get_uuid_univ_by_name_v1('University Name')
    Don't use this, because search fuction hardcoded on the client side instead of the server
    """
    def get_uuid_univ_by_name_v1(self, keyword):
        data = self.get_univ_by_name(keyword)
        id_sp = data[0]['id_sp']
        return id_sp

    """
    Get id_sp or uuid Univ V2
    Example a.get_uuid_univ_by_name_v2('University Name')
    """
    def get_uuid_univ_by_name_v2(self, keyword):
        data = self.search_pt(keyword)[0]
        id_sp = self.H.base64_decode(data['website-link'].replace('/data_pt/',''))
        return id_sp

    """
    Get website Univ
    Example a.get_univ_website_by_name('University Name')    
    Return website
    """
    def get_univ_website_by_name(self, keyword):
        data = self.search_pt(keyword)[0]
        return data['website-link']

    """
    Get id_sp or uuid Dosen
    Example a.get_uuid_dosen_by_name('Lecturer Name')
    """
    def get_uuid_dosen_by_name(self, keyword):
        data = self.search_dosen(keyword)
        id_sp = self.H.base64_decode(data[0]['website-link'].replace('/data_dosen/',''))
        return id_sp

    """
    Get website Dosen
    Example a.get_dosen_website_by_name('Ilham Riski Wibowo')
    Return website
    """
    def get_dosen_website_by_name(self, keyword):
        data = self.search_dosen(keyword)
        return data[0]['website-link'] 

    """
    Get id_sp or uuid Mahasiswa
    Example a.get_uuid_mahasiswa_by_name('Ilham Riski Wibowo')
    """
    def get_uuid_mahasiswa_by_name(self, keyword):
        data = self.search_mahasiswa(keyword)
        id_sp = self.H.base64_decode(data['mahasiswa'][0]['website-link'].replace('/data_mahasiswa/',''))
        return id_sp

    """
    Get website Mahasiswa
    Example a.get_mahasiswa_website_by_name('Ilham Riski Wibowo')
    Return website
    """
    def get_mahasiswa_website_by_name(self, keyword):
        data = self.search_mahasiswa(keyword)
        return data['mahasiswa'][0]['website-link']   

    # Detail
    ## Detail Pages Univ
    """
    Get detail Univ
    Data [akreditas_list [akreditas, tgl_akreditasi, tgl_berlaku], bujur, email, id_sp, internet, jln, kode_pos, laboratorium, lintag, listrik luas_tanah, nama_rektor, nama_wil, nm_lamb, no_fax, no_tel, npsn, perpustakaan, ruang_kelas, sk_pendirian_sp, stat_sp, tgl_berdiri, tgl_sk_pendirian_sp, website]
    Example a.detail_data_univ_by_name('University Name')
    """
    def detail_data_univ_by_name(self, keyword):
        uuid = self.get_univ_website_by_name(keyword)
        endpoint = self.api_version+uuid.replace('data_pt','detail_pt')
        return self.H.response(endpoint)

    """
    Get detail Univ Prodi
    Data [akreditas, id_sms, jenjang, kode_prodi, nm_lamb, rasio_list [dosen, mahasiswa],  stat_prodi]
    Example a.detail_data_univ_prodi_by_name('University Name')
    """
    def detail_data_univ_prodi_by_name(self, keyword):
        uuid = self.get_univ_website_by_name(keyword)
        endpoint = self.api_version+uuid.replace('data_pt','detail_pt_prodi')
        return self.H.response(endpoint)

    """
    Get detail Univ jumlah
    Data [jumlah_bidangilmu, jumlah_fakultas, jumlah_prodi, jumlah_prodi_akreditasi, rasio_list [dosen, mahasiswa]]
    Example a.detail_univ_jumlah_by_name('University Name')
    """
    def detail_univ_jumlah_by_name(self, keyword):
        uuid = self.get_univ_website_by_name(keyword)
        endpoint = self.api_version+uuid.replace('data_pt','detail_pt_jumlah')
        return self.H.response(endpoint) 


    """
    Get detail Univ Dosen
    Data [jumlah_dosen_jabatan [categories, series [data, nama]] jumlah_dosen_jenis_kelamin]
    Example a.detail_univ_dosen_by_name('University Name')
    """
    def detail_univ_dosen_by_name(self, keyword):
        uuid = self.get_univ_website_by_name(keyword)
        endpoint = self.api_version+uuid.replace('data_pt','detail_pt_dosen')
        return self.H.response(endpoint)

    """
    Get logo Univ
    Data Raw Image
    Example a.detail_univ_logo_by_name('University Name')
    """
    def detail_univ_logo_by_name(self, keyword):
        uuid = self.get_univ_website_by_name(keyword)
        endpoint = self.api_version+uuid.replace('data_pt','detail_pt_logo')
        return self.H.get_text(endpoint)

    ## Detail Page Dosen
    def detail_dosen_by_name(self, keyword):
        uuid = self.get_mahasiswa_website_by_name(keyword)
        endpoint = self.api_link+uuid.replace('/data_dosen','detail_dosen')
        return self.H.response(endpoint)

    ## Detail Page Prodi

    ## Detail Page Mahasiswa
    """
    Get detail Mahasiswa
    Data [datastatuskuliah [id_smt, nm_stat_mhs, sks_smt], datastudi [id_smt, kode_mk, nilai_huruf, nm_mk, sks_mk], dataumum [jk, ket_kelua, link_prodi, link_pt, mulai_smt, namajenjang, namaprodi, namapt, nipd, nm_jns_daftar, nama_pd, nm_prodi_asal, nm_pt_asal, no_seri_ijazah, reg_pd, sert_prof, tgl_keluar]]
    Example a.detail_mahasiswa_by_name('Ilham Riski Wibowo')
    """
    def detail_mahasiswa_by_name(self, keyword):
        uuid = self.get_mahasiswa_website_by_name(keyword)
        endpoint = self.api_link+uuid.replace('/data_mahasiswa','detail_mhs')
        return self.H.response(endpoint)


