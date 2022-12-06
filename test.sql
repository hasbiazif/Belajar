--cek nama bawahannya--
---erk_ekinerja_2021---
--cek nama bawahannya--
SELECT
	B.nip18,
	B.peg_nama,
	B.jumlah_aktivitas,
	B.atasan_nip,
	B.atasan_nama,
	B.eselon_nm,
	B.atasan_is_aktif,
	B.tmt_atasan_pensiun,
	B.status_atasan,
	B.atasan_sebagai_plt,
	( CASE WHEN B.opd IS NULL THEN vg3.satuan_kerja_nama ELSE B.opd END ) opd 
FROM
	(
	SELECT A
		.nip18,
		A.peg_nama,
		A.jumlah_aktivitas,
		A.atasan_nip,--data pegawai
		vg.peg_nama AS atasan_nama,--data atasan
		vg.eselon_nm,--data atasan
--data pegawai
		vg.peg_status AS atasan_is_aktif,--data atasan
		vg.peg_tmt_pensiun AS tmt_atasan_pensiun,--data atasan
		vg.peg_ketstatus AS status_atasan,--data atasan
-- 	( CASE WHEN A.atasan_nip IS NULL THEN vg2.nip_atasan END ) nip_atasan_plt,
-- 	( CASE WHEN A.atasan_nip IS NULL THEN vg2.nama_atasan END ) nama_atasan_plt,
	( CASE WHEN vg.tugas_tambahan_jabatan_id IS NOT NULL THEN concat ( 'PLT-', vg.tugas_tambahan_jabatan_id ) END ) atasan_sebagai_plt,
	(
	CASE
		
			WHEN vg.unit_kerja_nama_full ILIKE'%PENDIDIKAN WILAYAH I' THEN
			'KCD I' 
			WHEN vg.unit_kerja_nama_full ILIKE'%PENDIDIKAN WILAYAH II' THEN
			'KCD II' 
			WHEN vg.unit_kerja_nama_full ILIKE'%PENDIDIKAN WILAYAH III' THEN
			'KCD III' 
			WHEN vg.unit_kerja_nama_full ILIKE'%PENDIDIKAN WILAYAH IV' THEN
			'KCD IV' 
			WHEN vg.unit_kerja_nama_full ILIKE'%PENDIDIKAN WILAYAH V' THEN
			'KCD V' 
			WHEN vg.unit_kerja_nama_full ILIKE'%PENDIDIKAN WILAYAH VI' THEN
			'KCD VI' 
			WHEN vg.unit_kerja_nama_full ILIKE'%PENDIDIKAN WILAYAH VII' THEN
			'KCD VII' 
			WHEN vg.unit_kerja_nama_full ILIKE'%PENDIDIKAN WILAYAH VIII' THEN
			'KCD VIII' 
			WHEN vg.unit_kerja_nama_full ILIKE'%PENDIDIKAN WILAYAH IX' THEN
			'KCD IX' 
			WHEN vg.unit_kerja_nama_full ILIKE'%PENDIDIKAN WILAYAH X' THEN
			'KCD X' 
			WHEN vg.unit_kerja_nama_full ILIKE'%PENDIDIKAN WILAYAH XI' THEN
			'KCD XI' 
			WHEN vg.unit_kerja_nama_full ILIKE'%PENDIDIKAN WILAYAH XII' THEN
			'KCD XII' 
			WHEN vg.unit_kerja_nama_full ILIKE'%PENDIDIKAN WILAYAH XIII' THEN
			'KCD XIII' 
			WHEN vg.unit_kerja_nama_full ILIKE'%UPTD KHUSUS RUMAH SAKIT JIWA PROVINSI JAWA BARAT' THEN
			'DINKES - UPTD KHUSUS RUMAH SAKIT JIWA PROVINSI JAWA BARAT' 
			WHEN vg.unit_kerja_nama_full ILIKE'%UPTD KHUSUS RUMAH SAKIT UMUM DAERAH AL-IHSAN' THEN
			'DINKES - UPTD KHUSUS RUMAH SAKIT UMUM DAERAH AL-IHSAN' 
			WHEN vg.unit_kerja_nama_full ILIKE'%UPTD KHUSUS RUMAH SAKIT UMUM DAERAH JAMPANG KULON SUKABUMI' THEN
			'DINKES - UPTD KHUSUS RUMAH SAKIT UMUM DAERAH JAMPANG KULON SUKABUMI' 
			WHEN vg.unit_kerja_nama_full ILIKE'%UPTD KHUSUS RUMAH SAKIT UMUM DAERAH KESEHATAN KERJA PROVINSI JAWA BARAT' THEN
			'DINKES - UPTD KHUSUS RUMAH SAKIT UMUM DAERAH KESEHATAN KERJA PROVINSI JAWA BARAT' 
			WHEN vg.unit_kerja_nama_full ILIKE'%UPTD KHUSUS RUMAH SAKIT UMUM DAERAH PAMEUNGPEUK GARUT' THEN
			'DINKES - UPTD KHUSUS RUMAH SAKIT UMUM DAERAH PAMEUNGPEUK GARUT' 
			WHEN vg.unit_kerja_nama_full ILIKE'%UPTD LABORATORIUM KESEHATAN' THEN
			'DINKES - UPTD LABORATORIUM KESEHATAN' 
			WHEN vg.unit_kerja_nama_full ILIKE'%UPTD PELATIHAN KESEHATAN' THEN
			'DINKES - UPTD PELATIHAN KESEHATAN' 
			WHEN vg.unit_kerja_nama_full ILIKE'%UPTD RUMAH SAKIT PARU PROVINSI JAWA BARAT' THEN
			'DINKES - UPTD RUMAH SAKIT PARU PROVINSI JAWA BARAT' ELSE vg.organisasi_nama_alias 
		END 
		) opd 
	FROM
		(
		SELECT
			nip18,
			peg_nama,
			COUNT ( nip18 ) jumlah_aktivitas,
			(CASE WHEN nip_atasan is NULL THEN atasan_nip WHEN nip_atasan is NOT NULL THEN nip_atasan ELSE 'salah' END) atasan_nip
		FROM
			"isi_aktifitas"
			LEFT JOIN bulan_2.pegawai peg ON peg.peg_nip = isi_aktifitas.nip18 --edit disini
			LEFT JOIN struktur_bayangan_anggota sba ON sba.nip_bawahan = isi_aktifitas.nip18
			
		WHERE
			( tanggal BETWEEN '2022-11-01' AND '2022-11-30' ) 
			AND deleted_at IS NULL 
			AND status IS NULL 
			AND nip18 IN ( SELECT peg_nip FROM bulan_2.pegawai ) --edit disini
			
		GROUP BY
			nip18,
			peg_nama,
			status,
			atasan_nip,
			nip_atasan 
		) A 
		LEFT JOIN v_pegawai_data vg ON vg.peg_nip = A.atasan_nip
		LEFT JOIN v_pegawai_data vg2 ON vg2.peg_nip = A.nip18 
	WHERE
		vg2.is_gtk = 'f' -- 	AND atasan_nip = '198005151998102002'
		
	) B
	LEFT JOIN v_pegawai_data vg3 ON vg3.peg_nip = B.nip18 
ORDER BY
	B.atasan_nip
