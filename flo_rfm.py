
###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

###############################################################
# İş Problemi (Business Problem)
###############################################################
# FLO müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.
# Buna yönelik olarak müşterilerin davranışları tanımlanacak ve bu davranış öbeklenmelerine göre gruplar oluşturulacak..

###############################################################
# Veri Seti Hikayesi
###############################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından
# elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi

###############################################################
# GÖREVLER
###############################################################
import datetime as dt
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.float_format", lambda x: "%.2f" % x)
pd.set_option("display.width", 1000)


# GÖREV 1: Veriyi Anlama (Data Understanding) ve Hazırlama
           # 1. flo_data_20K.csv verisini okuyunuz.
           # 2. Veri setinde
                     # a. İlk 10 gözlem,
                     # b. Değişken isimleri,
                     # c. Betimsel istatistik,
                     # d. Boş değer,
                     # e. Değişken tipleri, incelemesi yapınız.
           # 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Herbir müşterinin toplam
           # alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
           # 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
           # 5. Alışveriş kanallarındaki müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların dağılımına bakınız.
           # 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
           # 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
           # 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.


df_ = pd.read_csv("datasets/flo_data_20k.csv")
df=df_.copy()
df.head()
# a. İlk 10 gözlem
df.head(10)
# b. Değişken isimleri
df.columns
#boyut
df.shape
# c. Betimsel istatistik
df.describe().T
# d. Boş değer
df.isnull().sum
# e. Değişken tipleri
df.info()

# 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Herbir müşterinin toplam
# alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
df["order_num_total"] = (df["order_num_total_ever_online"] + df["order_num_total_ever_offline"])
df["customer_value_total"] = (df["customer_value_total_ever_offline"]+ df["customer_value_total_ever_online"])

# 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
date_columns = [col for col in df.columns if "date" in col]
df[date_columns] = df[date_columns].apply(pd.to_datetime)

# 5. Alışveriş kanallarındaki müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların dağılımına bakınız.
df.groupby("order_channel").agg({"master_id": "count",
                                 "order_num_total": "sum",
                                 "customer_value_total": "sum"})


# 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
df.sort_values(by="customer_value_total", ascending=False)[:10]


# 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
df.sort_values(by="order_num_total", ascending=False)[:10]

# 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.
def create_rfm_prep(dataframe):
    dataframe["order_num_total"] = (dataframe["order_num_total_ever_online"]+ dataframe["order_num_total_ever_offline"])
    dataframe["customer_value_total"] = (dataframe["customer_value_total_ever_offline"]+ dataframe["customer_value_total_ever_online"])
    date_columns = [col for col in dataframe.columns if "date" in col]
    dataframe[date_columns] = dataframe[date_cols].apply(pd.to_datetime)
    return dataframe



# GÖREV 2: RFM Metriklerinin Hesaplanması

# Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi
df["last_order_date"].max() # 2021-05-30
analysis_date = dt.datetime(2021,6,1)
df["master_id"].value_counts()

# customer_id, recency, frequency ve monetarynin içinde olduğu yeni bir rfm dataframe oluşturmak lazım
rfm = pd.DataFrame()
rfm["customer_id"] = df["master_id"]
rfm["recency"] = (analysis_date - df["last_order_date"]).dt.days
rfm["frequency"] = df["order_num_total"]
rfm["monetary"] = df["customer_value_total"]

rfm.head()

# GÖREV 3: RF ve RFM Skorlarının Hesaplanması


rfm["recency_score"] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
rfm["frequency_score"] = pd.qcut(rfm['frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
rfm["monetary_score"] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm.head()


# recency_score ve frequency_score’u tek bir değişken olarak ifade edilmesi ve RF_SCORE olarak kaydedilmesi
rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))


# 3. recency_score ve frequency_score ve monetary_score'u tek bir değişken olarak ifade edilmesi ve RFM_SCORE olarak kaydedilmesi
rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str) + rfm['monetary_score'].astype(str))

rfm.head()


# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması

seg_map = {
    r"[1-2][1-2]": "hibernating",
    r"[1-2][3-4]": "at_Risk",
    r"[1-2]5": "cant_loose",
    r"3[1-2]": "about_to_sleep",
    r"33": "need_attention",
    r"[3-4][4-5]": "loyal_customers",
    r"41": "promising",
    r"51": "new_customers",
    r"[4-5][2-3]": "potential_loyalists",
    r"5[4-5]": "champions",
}

rfm["segment"] = rfm["RF_SCORE"].replace(seg_map, regex=True)
rfm.head()

# GÖREV 5: Aksiyon zamanı!
# 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])


 # 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv ye kaydediniz.

# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
# tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Sadık müşterilerinden(champions,loyal_customers),
# ortalama 250 TL üzeri ve kadın kategorisinden alışveriş yapan kişiler özel olarak iletişim kuralacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına
# yeni_marka_hedef_müşteri_id.cvs olarak kaydediniz.

target_segments_customer_ids = rfm[rfm["segment"].isin(["champions","loyal_customers"])]["customer_id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) &(df["interested_in_categories_12"].str.contains("KADIN"))]["master_id"]
cust_ids.to_csv("yeni_marka_hedef_müşteri_id.csv", index=False)
cust_ids.shape

rfm.head()

# b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşteri olan ama uzun süredir
# alışveriş yapmayan kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.cs
# olarak kaydediniz.
target_segments_customer_ids = rfm[rfm["segment"].isin(["cant_loose","hibernating","new_customers"])]["customer_id"]
cust_ids = df[(df["master_id"].isin(target_segments_customer_ids)) & ((df["interested_in_categories_12"].str.contains("ERKEK"))|(df["interested_in_categories_12"].str.contains("COCUK")))]["master_id"]
cust_ids.to_csv("indirim_hedef_müşteri_ids.csv", index=False)

# GÖREV 6: Tüm süreci fonksiyonlaştırınız.
###############################################################
# BONUS
###############################################################

def create_rfm(dataframe):
    # Veriyi Hazırlama
    dataframe["order_num_total"] = (
        dataframe["order_num_total_ever_online"]
        + dataframe["order_num_total_ever_offline"]
    )
    dataframe["customer_value_total"] = (
        dataframe["customer_value_total_ever_offline"]
        + dataframe["customer_value_total_ever_online"]
    )
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)

    # RFM METRIKLERININ HESAPLANMASI
    analysis_date = dt.datetime(2021, 6, 1)
    rfm = pd.DataFrame()
    rfm["customer_id"] = dataframe["master_id"]

    # DÜZELTİLEN SATIR: .dt.days doğrudan gün sayısını integer olarak alır
    rfm["recency"] = (analysis_date - dataframe["last_order_date"]).dt.days

    rfm["frequency"] = dataframe["order_num_total"]
    rfm["monetary"] = dataframe["customer_value_total"]

    # RF ve RFM SKORLARININ HESAPLANMASI
    rfm["recency_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(
        rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]
    )
    rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5])
    rfm["RF_SCORE"] = rfm["recency_score"].astype(str) + rfm[
        "frequency_score"
    ].astype(str)
    rfm["RFM_SCORE"] = (
        rfm["recency_score"].astype(str)
        + rfm["frequency_score"].astype(str)
        + rfm["monetary_score"].astype(str)
    )

    # SEGMENTLERIN ISIMLENDIRILMESI
    seg_map = {
        r"[1-2][1-2]": "hibernating",
        r"[1-2][3-4]": "at_Risk",
        r"[1-2]5": "cant_loose",
        r"3[1-2]": "about_to_sleep",
        r"33": "need_attention",
        r"[3-4][4-5]": "loyal_customers",
        r"41": "promising",
        r"51": "new_customers",
        r"[4-5][2-3]": "potential_loyalists",
        r"5[4-5]": "champions",
    }
    rfm["segment"] = rfm["RF_SCORE"].replace(seg_map, regex=True)

    return rfm[
        [
            "customer_id",
            "recency",
            "frequency",
            "monetary",
            "RF_SCORE",
            "RFM_SCORE",
            "segment",
        ]
    ]


rfm_df = create_rfm(df)
