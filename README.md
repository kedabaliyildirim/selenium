# Twitter Veri Kazımı

## Tweet Veri Yapısı

Twitter’ın API istekleri üzerinde yaptığı değişiklikler sonucunda hazırlanan bu program, Selenium kütüphanesini kullanarak Twitter’dan veri kazıyor. Şu anda çekilen veriler aşağıdaki gibidir:

tweet_text: tweet metini
replies: Kaç kişi yorum yapmış
retweet: kaç kişi retweet etmiş
likes: beğeni sayısı
created_at: tweetin oluşturulma tarihi ve saati
username: Kullanıcı adı (@vbo)

## Tweet Ön İşleme

Veriler ön işleme tabi tutuluyor. Bu ön işlemede Selenium kullanımından kaynaklanan kopya veriler kaldırılıyor; hashtag, mention ve web linkleri ayıklanıp kendi alanlarına yerleştiriliyor. Çekilen tarih verileri standardize ediliyor, metinler küçük harfe çevrilir, özel karakterler siliniyor, stopwords (sık kullanılan ve tek başına bir anlam ifade etmeyen kelimeler, örneğin "and", "the", "this" vs.) kelimeler ayıklanıyor, köklerine ayırma işlemi gerçekleştiriliyor.

## Kullanıcı Veri Yapısı

Username değişkeni elde edildikten sonra, her bir özel kullanıcı adı için ikinci bir veri kazıma başlatılıyor. Böylece Selenium driver fazla vakit kaybetmeden işlemleri tamamlayabiliyor. Kullanıcı veri yapısı aşağıdaki gibidir:

following: kullanıcı kaç kişiyi takip ediyor
follower: kullanıcıyı kaç kişi takip ediyor
posts: kullanıcı kaç paylaşım yapmış
Kullanıcı Verisi Ön İşleme
Kullanıcı verisi önce boş değerlerden arındırılıp, ondan sonra sayılarda bulunan k ve m gibi eklerden kurtarılıp sayılara (float) çevriliyor.

## Duygu Analizi ve Veri Kaydı

Veriler birleştirilerek basit duygu analizi gerçekleştiriliyor. Ardından veriler daha sonra kullanılmak üzere 4 ayrı CSV dosyasına kaydediliyor:

Cleaned_data: ön işleme tabi tutulmuş tweet verileri
User_data: işlenmiş kullanıcı verileri
Sentiment_data: tweet metni, duygu skoru ve duygu sınıfı alanlarından oluşan bir CSV
Merged_data: bütün verilerin birleştirilmiş halleri.

## Program Akışı

Programın girdi noktası main.py'dir:

1. Önce Bot oluşturulur
2. Twitter girişi
3. Arama modu seçimi ve arama işlemleri
4. Aranan sayfadaki içeriklerin çekilmesi ve DataFrame'e yerleştirilmesi
5. Tweet verilerinin ön işleme tabi tutulması
6. Özel (unique) kullanıcı isimlerini kullanarak kullanıcı verilerinin çekilmesi
7. Kullanıcı verilerinin ön işleme tabi tutulması
8. Tweet verileri ve kullanıcı verilerinin CSV dosyasına kaydedilmesi
9. Verilerin birleştirilmesi
10. Basit duygu analizi
11. Duygu analizi sonuçlarının diğer verilerle birleştirilmesi
12. Veri görselleştirme işlemleri

## Program Yapısı

### Bot (bot.py):

Bot objesi oluşturuluyor. İlk olarak bot objesi config.py dosyasından verileri çekiyor. Bu dosya projenin kökündeki gizli tutulması gereken .env dosyasında bulunan verileri alıyor. Bot objesi init_drive metodunu çağırarak gerekli ayarlamalarda bulunup (pencere açmadan çalışmak vs.) Firefox tarayıcısını başlatıyor. Bot objesinin içerisinde login ve close metodları bulunuyor. login metodu Twitter/login adresine giderek .env dosyasındaki TWITTER_HANDLE ve TWITTER_PASSWORD girdilerini kullanarak Twitter sitesine giriş yapıyor. close metodu Selenium driver'ı kapatmak için kullanılıyor.

### Config.py:

Sadece .env verilerini yüklüyor. Eğer .env yoksa projenin kökünde .env dosyasını oluşturun ve kullanıcı adınızı ve parolanızı buraya kaydedin.
Örnek:

    TWITTER_HANDLE=@example
    TWITTER_PASSWORD=123456

### Search.py:

Arama işlemlerinin gerçekleştiği yer. Giriş noktası search_selection fonksiyonu. Kullanıcıya hangi tip arama yapmak istediği soruluyor (basit ve gelişmiş). Seçilen aramaya göre search_basic veya search_advanced_initialization çağırılıyor. search_advanced_initialization arama formundaki doldurulacak alanları çeken search_advanced_param_getter fonksiyonunu çağırarak başlıyor ve search_param_initialization fonksiyonunu çağırarak arama işlemini tamamlıyor.

### Get_data.py:

Verilerin çekilmeye başlandığı yer. Bot objesi ile başlatılarak çalışan GetData sınıfı. Giriş noktası aggregate_tweet_data burada kullanıcıya iki soru ile başlanıyor: page_scroll_multiplier (sayfa kaydırılırken kaydırma mesafesi çarpanı, bunu artırmak kopya verileri azaltır ancak potansiyel veri kaybına sebep olabilir) ve max_scrolls (kaç adet sayfa aşağıya doğru kaydırılacak, bu değişkeni yüksek tutmak daha fazla veri sağlarken aynı zamanda gerekli zamanı da artırır). aggregate_tweet_data fonksiyonuna ek olarak iki ayrı fonksiyon daha var: get_tweets fonksiyonu burada tweet verileri çekilerek gerekli DataFrame formatına dönüştürülüyor ve get_user_data fonksiyonu aldığı username değişkeni ile gerekli aramaları yapıp kullanıcı verisini geri döndürüyor.

### Preprocess.py:

Bu dosyada gerekli ön işleme işlemleri hem tweet verileri hem de kullanıcı verileri için gerçekleştiriliyor user_preprocess ve tweet_preprocess fonksiyonları altında.

### Sentiment_analysis.py:

Burada TextBlob kütüphanesi kullanılarak basit duygu analizi gerçekleştiriliyor ve sentiment, sentiment_category, ve tweet_text alanlarını içeren DataFrame döndürülüyor.

### Analyze.py:

Bütün verilerin birleşmiş halleri veri görselleştirmesi için çalıştırılıyor. Giriş fonksiyonu create_all_plots kullanıcıya plotlar oluşturulsun mu diye soru sorup ona göre plotları oluşturuyor.
