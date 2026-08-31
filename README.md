# SAP ERP · Plotly chart kataloğu

Plotly ile bir SAP/ERP ortamında anlamlı olan **her chart türünden birer kısa örnek**. Veriler özet ve uydurmadır; amaç türü göstermek. SAP tablo/alan adları (VBAK, MBEW, BSID, …) gerçek nesnelerle eşlenmiştir.

## Galeriyi açmak

Hazır dosya:

```bash
python3 -m http.server 8000 --directory gallery
```

Tarayıcıda: [http://localhost:8000](http://localhost:8000)

Yeniden üretmek:

```bash
python3 -m pip install -r requirements.txt
python3 generate_gallery.py
python3 test_gallery.py
```

## Modüller

SD, MM, PP, QM, LE, FI, CO, CO-PA, PS, TR. Üstteki çiplerle süzülür, arama kutusu başlık / Plotly türü / SAP nesnesi arar.

Bilimsel 3D izler (cone, streamtube, volume, isosurface, quiver, carpet) ERP’ye denk gelmediği için yok.

## Dosyalar

| Dosya | Ne işe yarar |
| --- | --- |
| `sap_gallery/charts.py` | 71 chart üreticisi |
| `sap_gallery/index.template.html` | Galeri kabuğu |
| `generate_gallery.py` | `gallery/index.html` yazar |
| `test_gallery.py` | Her chart’ın figure ürettiğini doğrular |
