# Twitter Veri Kazım
Tweet Veri Yapısı
Twitter’ın APİ istekleri üzerinde yaptığı değişiklikler sonucunda hazırlanan bu program, selenium kütüphanesini kullanarak twitter’dan veri kazıyor, şu anda çekilen veriler aşağıdaki gibidir

    tweet_text: tweet metni
    replıes: Kaç kişi yorum yapmış
    retweet: kaç kişi retweetlemiş
    likes: beğeni sayısı
    created_at: tweetin oluşturulma tarihi ve saati 
    username: Kullanıcı adı (@vbo)

## Tweet Ön İşleme
Veriler ön işleme tabi tutuluyor bu ön işlemede selenium kullanımından kaynaklanan kopya veriler kaldırılıyor; hashtag mention ve web linkleri ayıklanıp kendi alanlarına yerleştiriliyor, çekilen tarih verileri standardize ediliyor, metinler küçük harfe çeviriliyor, özel karakterler siliniyor, stopwords (sık kullanılan ve tek başına bir anlam ifade etmeyen kelimeler bk. And, the, this vs.) kelimeler ayıklanıyor, köklerine ayırma işlemi gerçekleştiriliyor.

## Kullanıcı Veri Yapısı

username değişkeni elde edildikten sonra her bir özel kullanıcı adı için ikinci bir veri kazıma başlatılıyor, böylece selenium driver fazla vakit kaybetmeden işlemleri tamamlayabiliyor kullanıcı veris yapısı aşağıdaki gibidir.
    
    fallowıng: kullanıcı kaç kişiyi takip ediyor
    fallower: kullanıcıyı kaç kişi takip ediyor
    posts: kullanıcı kaç paylaşım yapmış

## Kullanıcı Verisi Ön İşleme

Kullanıcı verisi k ve m gibi eklerden kurtarılıp sayılara (float) çeviriliyor

## Duygu Analizi ve Veri Kaydı

Veriler Birleştirilerek basit duygu analizi gerçekleştiriliyor, ardından veriler daha sonra kullanılmak üzere 4 ayrı csv dosyasına kaydediliyor

    Cleaned_data: ön işleme tabi tutulmuş tweet verileri
    User_data: işlenmiş kullanıcı verileri
    Sentiment_data: tweet metni, duygu skoru ve duygu sınıfı alanlarından oluşan bir csv
    Merged_data: bütün verilerin birleştirilmiş halleri
