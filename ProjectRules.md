# GÖREV TANIMI
Sen kıdemli bir Full-Stack Mobil Geliştirici (React Native) ve Backend Mühendisisin (Django). Görevin, bir matematik öğretmeni (yani benim) için potansiyel özel ders öğrencisi (lead) toplayacak, "Porsuk: Sınav Koçu" adında, İsviçre Çakısı mantığında çok amaçlı bir eğitim uygulaması geliştirmektir. Ben hem bu uygulamanın geliştiricisi hem de tek yöneticisiyim. Geliştireceğin sistemde çoklu kullanıcı/öğretmen yapısına (multi-tenant) veya karmaşık yetkilendirmelere gerek yoktur. Sadece ben tek yetkili olacağım.

# TEKNOLOJİ YIĞINI (TECH STACK)
- **Frontend:** React Native (Expo Yönetimli İş Akışı - Hızlı geliştirme için)
- **State Management:** Zustand veya Redux Toolkit
- **Backend:** Python, Django, Django REST Framework (DRF)
- **Veritabanı:** PostgreSQL
- **Admin Panel:** Django Admin (Görselliği artırmak ve mobilden bile rahatça yönetebilmem için 'django-jazzmin' veya 'django-unfold' kütüphanesi kullanılacak)
- **Deployment:** Uygulama Coolify (VDS) üzerinde yayınlanacak şekilde Dockerize edilmelidir (Backend için Dockerfile ve docker-compose.yml hazırlanacak).

# BACKEND GEREKSİNİMLERİ (DİNAMİK YÖNETİM)
Sistemin tek hakimi benim. Mobil uygulamayı güncellemeye gerek kalmadan tüm içerikleri Django Admin üzerinden dinamik olarak yönetebilmeliyim. Lütfen şu Modelleri (Models) ve API Uç Noktalarını (Endpoints) oluştur:

1. **ExamDates (Sınav Tarihleri):** YKS, LGS, MSÜ gibi sınavların adları ve tarihleri. (Ana ekrandaki geri sayım sayacı buradan beslenecek).
2. **DailyQuestions (Günün Sorusu):** Tarih bazlı, resimli veya metin tabanlı matematik/zeka soruları ve benim Instagram Reels çözüm linklerim.
3. **DiagnosticTests (Teşhis Testleri):** "İşlem hatası mı, bilgi eksiği mi?" analizi yapacak dinamik test soruları ve ağırlıklı cevap şıkları.
4. **LeadContacts (Potansiyel Öğrenciler):** Uygulama içindeki iletişim butonlarına tıklayan veya test sonuçlarını gönderen öğrencilerin iletişim bilgilerinin ve eksik konularının düştüğü basit CRM tablosu.

# FRONTEND MİMARİSİ (REACT NATIVE)
Uygulama 'Bottom Tab Navigation' (Alt Gezinme Çubuğu) kullanmalıdır. 4 Ana Sekme olacak:

1. **Ana Ekran (Home):**
   - Üstte: API'den gelen dinamik Sınav Geri Sayım Sayacı.
   - Ortada: API'den gelen "Günün Zihin Açan Sorusu" kartı.
   - Altta: Basit, animasyonlu bir Pomodoro Sayacı (25dk çalışma / 5dk mola).

2. **Araçlar (Tools):** (İsviçre Çakısı Modülleri - Grid Yapısında)
   - Adım Adım Çarpanlara Ayırma Motoru.
   - Fonksiyon Grafiği Simülatörü.
   - İnteraktif Birim Çember.
   - Formül Sihirbazı (Dinamik Flashcardlar).

3. **Analiz (Analysis):**
   - Puan ve Sıralama Hesaplama Motoru (YKS/LGS).
   - Kazanma Simülatörü (Mevcut Net vs. Hedeflenen Okul farkı).
   - Teşhis Testi.
   - Hata Defteri (Hangi konularda hata yapıldığının loglanması).

4. **Destek (Support - Ana Dönüşüm Ekranı):**
   - Benim profesyonel öğretmen profilim, özgeçmişim ve Instagram linkim.
   - Büyük CTA (Call To Action) Butonu: "Hala kafan mı karışık? Ücretsiz Tanışma Seansı Ayarla" (Doğrudan benim WhatsApp API'me veya Calendly linkime yönlendirir).

# GELİŞTİRME KURALLARI VE ADIMLARI
Lütfen kodu tek seferde yazmaya çalışma. Geliştirmeyi aşağıdaki adımlara böl ve her adımı bitirdiğinde benden onay iste:

- **ADIM 1:** Backend (Django) projesinin başlatılması, PostgreSQL bağlantısı, modellerin (Models) yazılması ve 'django-jazzmin' ile şık bir Admin panelinin ayağa kaldırılması.
- **ADIM 2:** Django REST Framework ile API endpoint'lerinin (Sınav tarihleri, Günün sorusu vb.) yazılması.
- **ADIM 3:** Coolify deployment'ı için gerekli `Dockerfile`, `docker-compose.yml` ve `requirements.txt` dosyalarının ayarlanması.
- **ADIM 4:** React Native (Expo) projesinin başlatılması, klasör yapısının (components, screens, navigation, services) kurulması ve Bottom Tab Navigator'ın inşa edilmesi.
- **ADIM 5:** Frontend ana ekranlarının tasarlanması ve Backend API ile entegrasyonu (Axios kullanarak).
- **ADIM 6:** Özel araçların (Grafik, Birim Çember, Çarpanlara Ayırma) UI ve algoritmalarının kodlanması.

Lütfen bana projeyi yapılandırmak için hazır olduğunu bildir ve ADIM 1 ile kod yazmaya başla.