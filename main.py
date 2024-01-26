import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Notebook Sunumu
pd.options.display.float_format = '{:,.2f}'.format

# Veriyi Yükle
df_hh_income = pd.read_csv('Median_Household_Income_2015.csv', encoding="windows-1252")
df_pct_poverty = pd.read_csv('Pct_People_Below_Poverty_Level.csv', encoding="windows-1252")
df_pct_completed_hs = pd.read_csv('Pct_Over_25_Completed_High_School.csv', encoding="windows-1252")
df_share_race_city = pd.read_csv('Share_of_Race_By_City.csv', encoding="windows-1252")
df_fatalities = pd.read_csv('Deaths_by_Police_US.csv', encoding="windows-1252")

# Ön Veri Keşfi
# Görev 1: Her DataFrame için şekli, sütunları, NaN değerleri ve çiftleşenleri kontrol et
veri_tabloları = [df_hh_income, df_pct_poverty, df_pct_completed_hs, df_share_race_city, df_fatalities]
for df in veri_tabloları:
    print(f"DataFrame Şekli: {df.shape}")
    print(f"Sütunlar: {df.columns}")
    print(f"NaN Değerleri: {df.isna().sum()}")
    print(f"Çiftleşenler: {df.duplicated().sum()}")
    print("\n")

# Veri Temizleme - NaN Değerleri ve Çiftleşenleri Kontrol Etme
# Görev 2: NaN değerleri nasıl ele alacağınızı düşünün. Gerektiğinde 0 ile değiştirme.
# NaN değerlerini 0 ile doldurma, uygunsa
df_hh_income.fillna(0, inplace=True)
df_pct_poverty.fillna(0, inplace=True)
df_pct_completed_hs.fillna(0, inplace=True)
df_share_race_city.fillna(0, inplace=True)
df_fatalities.fillna(0, inplace=True)

# Her Bir ABD Eyaletinde Yoksulluk Oranını Gösteren Çubuk Grafiği
# Görev 3: Yoksulluk oranını her bir ABD eyaletinde en yüksekten en düşüğe sıralayan bir çubuk grafiği oluşturun.
yoksulluk_orani_grafik = px.bar(df_pct_poverty, x='Geographic Area', y='poverty_rate',
                                title='ABD Eyaletlerindeki Lise Mezuniyet Oranı',
                                labels={'poverty_rate': 'Yoksulluk Oranı (%)'})

yoksulluk_orani_grafik.update_layout(xaxis={'categoryorder': 'total descending'})
yoksulluk_orani_grafik.show()

# Her Bir ABD Eyaletindeki Lise Mezuniyet Oranını Gösteren Çubuk Grafiği
# Görev 4: ABD Eyaletleri'ni lise mezuniyet oranına göre artan sırayla gösterin.
lise_mezuniyet_grafik = px.bar(df_pct_completed_hs, x='Geographic Area', y='percent_completed_hs',
                               title='ABD Eyaletlerindeki Lise Mezuniyet Oranı',
                               labels={'percent_completed_hs': 'Lise Mezuniyet Oranı (%)'},
                               )
lise_mezuniyet_grafik.update_layout(xaxis={'categoryorder': 'total ascending'})
lise_mezuniyet_grafik.show()

# Yoksulluk Oranları ile Lise Mezuniyet Oranları Arasındaki İlişkiyi Gösteren Çizgi Grafiği
# Görev 5: İki y eksenli bir çizgi grafiği oluşturarak yoksulluk ve lise mezuniyet oranlarının birlikte hareket edip etmediğini gösterin.
yoksulluk_lise_iliski = px.line(df_pct_poverty, x='Geographic Area', y='poverty_rate',
                               title='Yoksulluk ve Lise Mezuniyet Oranları Arasındaki İlişki',
                               labels={'poverty_rate': 'Yoksulluk Oranı (%)'},
                               )
yoksulluk_lise_iliski.update_layout(xaxis={'categoryorder': 'total ascending'})

# Convert 'poverty_rate' to numeric
df_pct_poverty['poverty_rate'] = pd.to_numeric(df_pct_poverty['poverty_rate'], errors='coerce')

# Seaborn .jointplot() Kullanımı
joint_grafik = sns.jointplot(data=df_pct_poverty, x='poverty_rate', y='poverty_rate', kind='kde')

# Görselleştirmeyi göster
plt.show()

# Seaborn .lmplot() Kullanımı
lm_grafik = sns.lmplot(data=df_pct_poverty, x='poverty_rate', y='poverty_rate')

# lmplot için show kullanabilirsiniz
lm_grafik.fig.show()

# Her Bir ABD Eyaletindeki Rasyal Yapıyı Gösteren Alt Sektörlü Çubuk Grafiği
# Görev 6: Her bir ABD eyaletinde beyaz, siyah, latino, asyalı ve kızılderili nüfusun payını gösteren bir çubuk grafiği oluşturun.
rasyal_yapi_grafik = px.bar(df_share_race_city, x='Geographic area', y=['share_white', 'share_black', 'share_hispanic', 'share_asian', 'share_native_american'],
                            title='Her Bir ABD Eyaletindeki Rasyal Yapı',
                            labels={'value': 'Nüfus Payı (%)', 'variable': 'Ras'},
                            )
rasyal_yapi_grafik.show()

# Rasa Göre Ölen Kişilerin Donut Grafiği
# Görev 7: .value_counts() kullanarak bir donut grafiği oluşturun.
rasya_donut_grafik = df_fatalities['race'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, wedgeprops=dict(width=0.3))
plt.axis('equal')  # Eşit en-boy oranı, pastanın bir daire olarak çizilmesini sağlar.
plt.title('Rasa Göre Ölen Kişiler')
plt.show()

# Erkekler ve Kadınların Toplam Ölüm Sayısını Karşılaştıran Bir Çizgi Grafiği
# Görev 8: Erkeklerin kadınlardan ne kadar daha fazla öldüğünü göstermek için df_fatalities kullanın.
cinsiyet_grafik = px.histogram(df_fatalities, x='gender', title='Erkekler ve Kadınların Toplam Ölüm Sayısı',
                                labels={'gender': 'Cinsiyet', 'count': 'Ölüm Sayısı'},
                                )
cinsiyet_grafik.show()

# Yaş ve Ölüm Şeklini Gösteren Bir Kutu Grafiği
# Görev 9: Veriyi cinsiyete göre ayırın ve ölüm şeklinde bir farklılık olup olmadığını kontrol edin.
yas_olum_kutu_grafik = px.box(df_fatalities, x='gender', y='age', color='manner_of_death',
                              title='Cinsiyet ve Ölüm Şekli İle Yaş',
                              labels={'gender': 'Cinsiyet', 'age': 'Yaş', 'manner_of_death': 'Ölüm Şekli'},
                              )
yas_olum_kutu_grafik.show()

# Silah Taşıyanlar
# Görev 10: Polis öldürmelerinin kaçında insanlar silahlıydı? Hangi tür silahın (varsa) ölen kişinin elinde olduğunu gösteren bir grafik oluşturun.
silah_yuzdesi = (df_fatalities['armed'].value_counts(normalize=True) * 100).plot(kind='bar')
silah_yuzdesi.set_ylabel('Yüzde')
silah_yuzdesi.set_title('Polis Öldürmelerinin Kaçında İnsanlar Silahlıydı?')
plt.show()

# Kaç Yaşında Ölen Kişiler?
# Görev 11: Ölen kişilerin kaç yüzde 25 yaşın altında olduğunu bulun.
_yas_alti_yuzdesi = (df_fatalities['age'] < 25).value_counts(normalize=True) * 100

# Histogram ve KDE Grafiği Oluştur
plt.figure(figsize=(10, 6))
sns.histplot(df_fatalities['age'], kde=True)
plt.title('Polis Tarafından Öldürülen Kişilerin Yaş Dağılımı')
plt.xlabel('Yaş')
plt.ylabel('Frekans')
plt.show()

# Her bir rasa göre ayrı bir KDE grafiği oluştur
plt.figure(figsize=(14, 8))
for rasa in df_fatalities['race'].unique():
    sns.kdeplot(df_fatalities[df_fatalities['race'] == rasa]['age'], label=rasa)
plt.title('Polis Tarafından Öldürülen Kişilerin Yaş Dağılımı Rasa Bazında')
plt.xlabel('Yaş')
plt.ylabel('Yoğunluk')
plt.legend()
plt.show()

# Ölen Kişilerin Rasyal Dağılımını Gösteren Çubuk Grafiği
# Görev 12: Her bir rasa göre toplam ölen kişi sayısını gösteren bir çubuk grafiği oluşturun.
rasa_toplam_grafik = df_fatalities['race'].value_counts().plot(kind='bar')
rasa_toplam_grafik.set_ylabel('Ölüm Sayısı')
rasa_toplam_grafik.set_title('Toplam Ölen Kişi Sayısı Rasa Bazında')
plt.show()

# Akıl Hastalığı ve Polis Öldürmeleri
# Görev 13: Polis tarafından öldürülen kişilerin kaçının akıl hastalığı teşhisi konulmuş?
akil_hastalik_yuzdesi = (df_fatalities['signs_of_mental_illness'].value_counts(normalize=True) * 100).plot(kind='bar')
akil_hastalik_yuzdesi.set_ylabel('Yüzde')
akil_hastalik_yuzdesi.set_title('Polis Tarafından Öldürülen Kişilerin Kaçında Akıl Hastalığı Teşhisi Var?')
plt.show()

# En Fazla Polis Öldürmenin Gerçekleştiği Şehirler
# Görev 14: En fazla polis öldürmenin gerçekleştiği ilk 10 şehri sıralayan bir grafik oluşturun.
en_fazla_sehirler_grafik = df_fatalities['city'].value_counts().head(10).plot(kind='barh')
en_fazla_sehirler_grafik.set_xlabel('Ölüm Sayısı')
en_fazla_sehirler_grafik.set_title('En Fazla Polis Öldürmenin Gerçekleştiği Top 10 Şehir')
plt.show()

# Rasa Göre Ölüm Oranı
# Görev 15: Her bir rasanın en fazla 10 şehirdeki payını bulun.
rasa_oran_top_sehirler = df_fatalities[df_fatalities['city'].isin(df_fatalities['city'].value_counts().head(10).index)]['race'].value_counts(normalize=True).plot(kind='bar')
rasa_oran_top_sehirler.set_ylabel('Yüzde')
rasa_oran_top_sehirler.set_title('En Fazla 10 Şehirdeki Polis Öldürmelerinin Rasa Oranı')
plt.show()

# ABD Eyaletleri Bazında Polis Öldürmelerini Gösteren Bir Choropleth Haritası
# Görev 16: Hangi eyaletler en tehlikeli? Haritanızı önceki grafiğinizle karşılaştırın.
harita = px.choropleth(df_fatalities['state'].value_counts(), locations=df_fatalities['state'].value_counts().index,
                        locationmode='USA-states', color=df_fatalities['state'].value_counts().values,
                        color_continuous_scale='Viridis', title='ABD Eyaletleri Bazında Polis Öldürmeleri')
harita.update_geos(scope='usa')
harita.show()

# Zaman İçindeki Polis Öldürmelerinin Sayısını Analiz Etme
# Görev 17: Zaman içindeki polis öldürmelerinin sayısını analiz edin. Veride bir trend var mı?
zaman_grafik = px.histogram(df_fatalities, x='date', nbins=100, title='Zaman İçindeki Polis Öldürmelerinin Sayısı')
zaman_grafik.update_layout(xaxis_title='Tarih', yaxis_title='Ölüm Sayısı')
zaman_grafik.show()