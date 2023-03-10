# -*- coding: utf-8 -*-
"""MachineLearningTerapan_ProjekPertama.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17WEwPFouEnQZo159QpRm-bDUsVRUqbSC

# Solar Generation Data - Predictive Analysis

## Domain Proyek

Energi terbarukan menjadi alternatif yang banyak dipakai untuk menggantikan sumber energi konvensional, seperti minyak bumi dan batu bara. Keunggulan dari sumber energi ini, selain tidak akan habis, adalah rendahnya residu dari proses pembangkitan listrik. Residu yang dimaksud seperti gas rumah kaca dari pembakaran batu bara pada Pembangkit Listrik Tenaga Uap (PLTU), yang berbahaya bagi lingkungan dan dapat menyebabkan pemanasan global. Oleh karena itu, berbagai *stakeholder* terus berupaya meningkatkan porsi pemanfaatan sumber energi terbarukan dalam memenuhi kebutuhan energi.

Salah satu jenis energi terbarukan yang populer adalah energi surya. Energi ini memiliki kapasitas pembangkitan yang terus meningkat dari tahun ke tahun [1, 2]. Selain itu, implementasi energi surya, seperti dengan panel Photo-Voltaic (PV), mengalami penurunan biaya dari tahun ke tahun [3]. Penelitian dalam bidang pembangkitan energi surya, material panel PV, dan teknologi pengumpulan energi surya juga telah banyak dilakukan [4]. Hal ini menunjukkan potensi energi surya untuk mengurangi konsumsi energi dari sumber konvensional dan tidak ramah lingkungan.

Hal yang perlu diperhatikan adalah kapasitas energi yang dihasilkan energi surya belum bisa sepenuhnya menggantikan sumber energi konvensional. Oleh karena itu, ketika sebuah Pembangkit Listrik Tenaga Surya (PLTS) dihubungkan ke jaringan distribusi listrik (*grid*), energi yang diproduksi PLTS harus dapat disesuaikan dengan energi dari PLTU atau pembangkit lain. Apabila seluruh pembangkit memproduksi energi tanpa memperhatikan kondisi atau kapasitas jaringan, hal ini dapat membahayakan seluruh grid.

Di sinilah pentingnya model untuk memprediksi produksi energi surya pada PLTS. Apabila energi yang dihasilkan dapat diketahui *trend*-nya, pihak yang mengoperasikan grid dapat dengan mudah mencegah *overcapacity* atau *under-capacity*. Energi surya pada akhirnya dapat membantu memenuhi konsumsi energi tanpa menyebabkan kerusakan atau gangguan pada grid. Hal yang dibutuhkan adalah model prediksi pembangkitan energi listrik dari PLTS yang akurat. Di proyek ini, akan dibentuk model prediksi yang dapat dimanfaatkan untuk kepentingan tersebut dengan mengamati penelitian yang telah ada [5,6]. 
<br>
<br>

**Referensi:** <br>
[1] REN21, P.S., Renewables 2014: Global Status Report. 2014: Secretariat
Renewable Energy Policy Network for the 21st Century (REN21) Paris. <br>
[2] International Energy Agency, International Energy Statistics. 2014; Available
from: ???http://www.eia.gov/cfapps/ipdbproject/IEDIndex3.cfm???. <br>
[3] Price of crystaline silicon photovoltaic cells; 2012. Available from: ???http://
www.economist.com/blogs/graphicdetail/2012/12/daily-chart-19??? <br>
[4] Kannan, N., & Vakeesan, D. (2016). Solar energy for future world:-A review. Renewable and Sustainable Energy Reviews, 62, 1092-1105. <br>
[5] Sharma, N., Sharma, P., Irwin, D., & Shenoy, P. (2011, October). Predicting solar generation from weather forecasts using machine learning. In 2011 IEEE international conference on smart grid communications (SmartGridComm) (pp. 528-533). IEEE. <br>
[6] Yesilbudak, M., ??olak, M., & Bayindir, R. (2016, November). A review of data mining and solar power prediction. In 2016 IEEE International Conference on Renewable Energy Research and Applications (ICRERA) (pp. 1117-1121). IEEE.

## Business Understanding

### Problem Statement

Pembangkit Listrik Tenaga Surya menghasilkan energi secara fluktuatif dan tidak dapat dikendalikan. Setiap pembangkit yang dihubungkan ke jaringan distribusi listrik (*grid*) perlu diatur sedemikian rupa sehingga tidak menyebabkan gangguan/kerusakan. Oleh karena itu, energi dari PLTS harus dapat diprediksi agar membantu pengaturan PLTS ketika dihubungkan dengan grid

### Goals

Proyek ini bertujuan untuk menghasilkan model prediksi dari produksi energi PLTS dengan memanfaatkan data pengamatan cuaca.

### Solution Statement

Untuk memenuhi tujuan tersebut, akan diajukan empat model regresi:
1.   Support Vector Machine (SVM)
2.   Random Forest
3.   Adaptive Boosting
4.   Gradient Boosting

Masing-masing model akan dibandingkan kinerjanya dengan metrik R<sup>2</sup>.

## Data Understanding Part 1

Dataset yang akan digunakan adalah data dua PLTS di India selama 34 hari. Setiap PLTS menghasilkan data pembangkitan daya pada level inverter dan data pembacaan sensor pada array PV. Data ini dapat diunduh dari [Kaggle](https://www.kaggle.com/datasets/anikannal/solar-power-generation-data?select=Plant_2_Generation_Data.csv).
"""

# Commented out IPython magic to ensure Python compatibility.
# Import Required Library
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

# Mount Gdrive
from google.colab import drive

drive.mount('/content/gdrive/', force_remount=True)

"""### Dataset 1

Dataset pertama adalah data pembangkitan daya PLTS. Di sini, terdapat beberapa variabel:
* DATE_TIME: Waktu pengamatan dengan interval 15 menit;
* PLANT_ID: Nomor identitas PLTS;
* SOURCE_KEY: Kode identitas inverter;
* DC_POWER: jumlah daya DC yang dihasilkan inverter tiap 15 menit (kiloWatt);
* AC_POWER: jumlah daya AC yang dihasilkan inverter tiap 15 menit (kiloWatt);
* DAILY_YIELD: jumlah kumulatif energi yang dipanen inverter pada hari tersebut (kWh);
* TOTAL_YIELD: jumlah energi yang dipanen inverter hingga waktu tersebut (kWh)
"""

# Load data
data1 = pd.read_csv("/content/gdrive/MyDrive/Training/Dicoding/Dataset/Plant_2_Generation_Data.csv")
data1.head(10)

data1.tail(10)

"""**EDA**"""

data1.info()

data1.describe()

data1[["PLANT_ID"]].value_counts()

data1[["DATE_TIME"]].value_counts()

data1.isnull().any()

"""**Visualisasi**"""

num_columns = data1.columns.to_list()[3:]

plt.figure(figsize = (10,10))
for i, column in enumerate(num_columns):
  plt.subplot(2,2,i+1)
  data1[column].hist(edgecolor='black', bins=50)
  plt.title("{}".format(column))

plt.tight_layout()
plt.show()

plt.figure(figsize = (10,10))
for i, column in enumerate(num_columns):
  plt.subplot(2,2,i+1)
  sns.boxplot(data=data1[column])
  plt.title("{}".format(column))

plt.tight_layout()
plt.show()

sns.pairplot(data=data1[num_columns])
plt.tight_layout()
plt.show()

sns.heatmap(data=data1[num_columns].corr(), annot=True)
plt.tight_layout()
plt.show()

"""### Dataset 2

Dataset kedua adalah data pembacaan sensor di array PV PLTS. Di sini, terdapat beberapa variabel:
* DATE_TIME: Waktu pengamatan dengan interval 15 menit;
* PLANT_ID: Nomor identitas PLTS;
* SOURCE_KEY: Kode identitas sensor;
* AMBIENT_TEMPERATURE: suhu ambient PLTS (derajat Celcius);
* MODULE_TEMPERATURE: suhu module PV (derajat Celcius);
* IRRADIATION: jumlah iradiasi setiap 15 menit (W/m<sup>2</sup>)
"""

# Load data
data2 = pd.read_csv("/content/gdrive/MyDrive/Training/Dicoding/Dataset/Plant_2_Weather_Sensor_Data.csv")
data2.head(10)

data2.tail(10)

"""**EDA**"""

data2.info()

data2.describe()

data2[["PLANT_ID"]].value_counts()

data2[["DATE_TIME"]].value_counts()

data2.isnull().any()

"""**Visualisasi**"""

num_columns2 = data2.columns.to_list()[3:]

plt.figure(figsize = (10,10))
for i, column in enumerate(num_columns2):
  plt.subplot(3,1,i+1)
  data2[column].hist(edgecolor='black', bins = 50)
  plt.title("{}".format(column))

plt.tight_layout()
plt.show()

plt.figure(figsize = (10,10))
for i, column in enumerate(num_columns2):
  plt.subplot(3,1,i+1)
  sns.boxplot(data=data2[column])
  plt.title("{}".format(column))

plt.tight_layout()
plt.show()

sns.pairplot(data=data2[num_columns2])
plt.tight_layout()
plt.show()

sns.heatmap(data=data2[num_columns2].corr(), annot=True)
plt.tight_layout()
plt.show()

"""## Data Understanding Part 2

### Filtering

Pada dua dataset yang digunakan, daat diketahui bahwa dataset diperoleh dari dua sensor berbeda, tetapi pada rentang waktu yang sama. Selain itu, pada Dataset 1, jumlah pembacaan sensor untuk satu waktu tertentu berjumlah lebih dari satu. Oleh karena itu, di sini, Dataset 1 akan dicari **nilai rata-rata (*mean*)** untuk satu waktu spesifik.
"""

dc_power = []
ac_power = []
daily_yield = []
total_yield = []

for time in data1["DATE_TIME"].unique().tolist():
  dc_power.append(data1.loc[data1["DATE_TIME"] == time, ["DC_POWER"]].mean().to_list())
  ac_power.append(data1.loc[data1["DATE_TIME"] == time, ["AC_POWER"]].mean().to_list())
  daily_yield.append(data1.loc[data1["DATE_TIME"] == time, ["DAILY_YIELD"]].mean().to_list())
  total_yield.append(data1.loc[data1["DATE_TIME"] == time, ["TOTAL_YIELD"]].mean().to_list())

dc_power = np.array(dc_power)
dc_power.shape

ac_power = np.array(ac_power)
ac_power.shape

daily_yield = np.array(daily_yield)
daily_yield.shape

total_yield = np.array(total_yield)
total_yield.shape

"""### Gabungkan Data

Kedua dataset di atas kemudian dapat digabungkan untuk menghasilkan satu dataset baru. Hal ini untuk memudahkan pengolahan data lebih lanjut.
"""

data2["DC_POWER"] = dc_power
data2["AC_POWER"] = ac_power
data2["DAILY_YIELD"] = daily_yield
data2["TOTAL_YIELD"] = total_yield

data2.head()

"""### Konversi Tipe Data

Pada pengecekan tipe data tiap kolom, data pada kolom DATE_TIME masih berupa object. Oleh karena itu, data pada kolom tersebut perlu dikonversi menjadi tipe data datetime.
"""

data2["DATE_TIME"] = pd.to_datetime(data2["DATE_TIME"])

data2.head()

data2.dtypes

"""### Drop Irrelevant Column

Data identitas PLTS dan sensor tidak digunakan untuk melatih model sehingga dapat dibuang.
"""

data3 = data2.drop(['PLANT_ID', 'SOURCE_KEY'], axis = 1)
data3.head()

"""### Check New Dataset

Setelah dilakukan beberapa pengolahan, dataset baru dapat dicek. Untuk memudahkan, visualisasi dengan *pairplot, heatmap, dan boxplot* dilakukan. Informasi dari masing-masing plot adalah sebagai berikut:
* Pairplot: informasi distribusi data,
* Heatmap: informasi korelasi setiap fitur,
* Boxplot: informasi terkait *outliers*
"""

data3.info()

data3.describe()

num_columns3 = data3.columns.to_list()[1:]

sns.pairplot(data=data3[num_columns3])
plt.tight_layout()
plt.show()

plt.figure(figsize=(10,10))
sns.heatmap(data=data3[num_columns3].corr(), annot=True)
plt.tight_layout()
plt.savefig('heatmap2.png')
plt.show()

plt.figure(figsize = (10,10))
for i, column in enumerate(num_columns3):
  plt.subplot(4,2,i+1)
  sns.boxplot(data=data3[column])
  plt.title("{}".format(column))

plt.tight_layout()
plt.savefig('boxplot.png')
plt.show()

"""### Drop Uncorrelated Column

Melalui Heatmap, dapat diketahui bahwa data pada kolom TOTAL_YIELD memiliki korelasi yang rendah dengan data pada kolom lain karena mendekati nol. Oleh larena itu, data di kolom ini dapat dibuang.
"""

data4 = data3.drop(['TOTAL_YIELD'], axis = 1)
data4.head()

"""### Remove Outliers

Dari boxplot, masih terdapat outliers pada kolom MODULE_TEMPERATURE dan IRRADIATION. Oleh karena itu, untuk membersihkannya, akan digunakan metode IQR.
"""

num_columns4 = data4.columns.to_list()[1:]

Q1 = data4.quantile(0.25)
Q3 = data4.quantile(0.75)
IQR=Q3-Q1
data5 = data4[~((data4[num_columns4]<(Q1-1.5*IQR))|(data4[num_columns4]>(Q3+1.5*IQR))).any(axis=1)]
 
data5.shape

"""### Check New Dataset Part 2"""

plt.figure(figsize = (10,10))
for i, column in enumerate(num_columns4):
  plt.subplot(3,2,i+1)
  sns.boxplot(data=data5[column])
  plt.title("{}".format(column))

plt.tight_layout()
plt.show()

sns.pairplot(data=data5[num_columns4])
plt.tight_layout()
plt.savefig('pairplot2.png')
plt.show()

"""### Remove Zero Values

Setelah mengecek ulang data, dapat diketahui dari pairplot bahwa kolom AC_POWER, DC_POWER, dan IRRADIATION memiliki nilai nol yang banyak. Oleh karena itu, di sini, data tersebut akan dihilangkan.
"""

data6 = data5.loc[(data5[['AC_POWER','DC_POWER','IRRADIATION']]!=0).all(axis=1)]
 
data6.shape

sns.pairplot(data=data6[num_columns4])
plt.tight_layout()
plt.savefig('pairplot.png')
plt.show()

plt.figure(figsize=(10,10))
sns.heatmap(data=data6[num_columns4].corr(), annot=True)
plt.tight_layout()
plt.savefig('heatmap.png')
plt.show()

"""## Data Preparation

### Principal Component Analysis

Dari pairplot dan heatmap, dapat diketahui bahwa data AC_POWER dan DC_POWER memiliki korelasi yang sangat tinggi. Oleh karena itu, untuk mengurangi dimensi data, akan dilakukan PCA terhadap dua kolom tersebut. Hasilnya adalah sebuah fitur agregat bernama OUTPUT_POWER.
"""

from sklearn.decomposition import PCA
 
pca = PCA(n_components=2, random_state=42)
pca.fit(data6[["DC_POWER", "AC_POWER"]])
pca.explained_variance_ratio_.round(3)

pca2 = PCA(n_components = 1, random_state=42)
pca2.fit(data6[["DC_POWER", "AC_POWER"]])
data6['OUTPUT_POWER'] = pca2.transform(data6.loc[:, ('DC_POWER','AC_POWER')]).flatten()
data6.drop(['DC_POWER','AC_POWER'], axis=1, inplace=True)

data6.head()

"""### Train-Test Split

Setelah data siap, akan dilakukan pembagian dataset untuk kebutuhan pelatihan dan evaluasi. Di sini, data akan dibagi dengan rasio 80:20. Label atau nilai yang akan diprediksi adalah DAILY_YIELD, yaitu total energi yang dipanen secara harian. Kolom sisanya akan menjadi fitur untuk latihan. Selain itu, data DATE_TIME tidak akan digunakan sehingga dapat dibuang.
"""

from sklearn.model_selection import train_test_split
 
X = data6.drop(["DATE_TIME", "DAILY_YIELD"], axis =1)
y = data6["DAILY_YIELD"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)

print(f'Total # of sample in whole dataset: {len(X)}')
print(f'Total # of sample in train dataset: {len(X_train)}')
print(f'Total # of sample in test dataset: {len(X_test)}')

"""### Scaling

Fitur data latih memiliki rentang nilai yang berbeda-beda. Hal ini dapat meningkatkan kesalahan dari model sewaktu pelatihan. Oleh karena itu, data latih akan dilakukan Min-Max Scaling untuk mengubah setiap fitur menjadi dalam rentang [0,1]. Data uji akan dilakukan scaling secara terpisah untuk mencegah kebocoran data.
"""

from sklearn.preprocessing import MinMaxScaler
 
num_columns5 = X.columns.to_list()
scaler = MinMaxScaler()
scaler.fit(X_train[num_columns5])
X_train[num_columns5] = scaler.transform(X_train.loc[:, num_columns5])
X_train[num_columns5].head()

"""## Model Development

Hal pertama yang dilakukan adalah mempersiapkan DataFrame untuk membandingkan kinerja model.
"""

models = pd.DataFrame(index=['train_r2', 'test_r2'], 
                      columns=['SVM', 'RandomForest', 'AdaBoost', 'GradBoost'])

"""### Random Forest

Model pertama yang digunakan adalah Random Forest. Model ini adalah model ensmble (gabungan) dari model-model individu (estimator), seperti Decision Tree. Model ini akan menjalankan prediksi secara pararel.

Di sini, parameter yang digunakan untuk model Random Forest adalah jumlah estimator (n_estimators) dan kedalaman pohon maksimal (max_depth). Untuk memperoleh parameter terbaik digunakan metode Grid Search yang menghasilkan parameter:
* n_estimators = 100
* max_depth = 32

Pada model ini dan model selanjutnya juga terdapat parameter random_state yang digunakan untuk mengatur random number generator sehingga model akan selalu memiliki output yang sama.
"""

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor

model1 = RandomForestRegressor()
parameters1 = {
    'n_estimators' : [25, 50, 100, 150, 200],
    'max_depth' : [4, 8, 16, 32, 64]
}

rf_grid = GridSearchCV(model1, parameters1, cv = 5)

rf_grid.fit(X_train, y_train)

rf_grid.best_params_

rf_grid.best_score_

from sklearn.metrics import r2_score
 
RF = RandomForestRegressor(n_estimators=100, max_depth=32, random_state=42, n_jobs=-1)
RF.fit(X_train, y_train)
 
models.loc['train_r2','RandomForest'] = r2_score(y_pred=RF.predict(X_train), y_true=y_train)

"""### SVM

Model kedua yang digunakan adalah Support Vector Machine (SVM). Tujuan dari model ini adalah mencari hyperplane yang memiliki margin paling besar. 

Pada SVM terdapat beberapa parameter. Pertama, kernel adalah fungsi yang digunakan untuk memetakan data berdimensi rendah ke dimensi yang lebih tiggi. Kedua, gamma adalah koefisien dari kernel. Ketiga, C adalah parameter regularisasi. Dengan Grid Search, diperoleh parameter terbaik:
* kernel = poly
* gamma = 1
* C = 1
"""

from sklearn.svm import SVR

model2 = SVR()
parameters2 = {
    'C' : [0.1, 0.2, 0.5, 1],
    'kernel' : ['linear', 'poly', 'rbf'],
    'gamma' : [0.01 , 0.1, 1]
}

svm_grid = GridSearchCV(model2, parameters2, cv = 5)

svm_grid.fit(X_train, y_train)

svm_grid.best_params_

svm_grid.best_score_

svr = SVR(kernel='poly', gamma = 1, C=1)
svr.fit(X_train, y_train)

models.loc['train_r2','SVM'] = r2_score(y_pred=svr.predict(X_train), y_true=y_train)

"""### Adaptive Boosting

Adaptive Boosting (AdaBoost) adalah model ensemble seperti Random Forest. Perbedaannya, model dilatih secara sekuensial dengan menggabungkan model-model lemah menjadi model yang lebih kuat.

Di sini, terdapat beberapa perameter yang digunakan. Pertama, n_estimators adalah jumlah model individu yang digabungkan. Kedua, learning_rate yaitu bobot yang dikenakan ke regressor tiap iterasi. Ketiga, loss yaitu fungsi loss yang digunakan untuk mengubah bobot tiap iterasi. Di sini, dengan Grid Search diperoleh parameter terbaik:
* learning_rate = 0.1
* n_estimators = 25
* loss = linear
"""

from sklearn.ensemble import AdaBoostRegressor

model3 = AdaBoostRegressor()
parameters3 = {
    'n_estimators' : [25, 50, 100, 150, 200],
    'learning_rate' : [0.01, 0.05, 0.1, 0.5, 1],
    'loss' : ['linear', 'square', 'exponential']
}

adaboost_grid = GridSearchCV(model3, parameters3, cv = 5)

adaboost_grid.fit(X_train, y_train)

adaboost_grid.best_params_

adaboost_grid.best_score_

adaboosting = AdaBoostRegressor(learning_rate=0.1, loss='linear', n_estimators = 25, random_state=42)                             
adaboosting.fit(X_train, y_train)
models.loc['train_r2','AdaBoost'] = r2_score(y_pred=adaboosting.predict(X_train), y_true=y_train)

"""### Gradient Boosting

Gradient Boosting (GradBoost) adalah varian algoritma Boosting seperti AdaBoost. Perbedaannya, GradBoost merupakan algoritma yang lebih umum sehingga lebih fleksibel untuk diapliaksikan ke setiap kasus.

Pada kasus ini, parameter yang digunakan adalah:
* n_estimators, yaitu jumlah model individu
* learning_rate, yaitu ukuran mengecilnya kontribusi estimator tiap iterasi
* loss, fungsi loss yang dioptimisasi
* subsample, ukuran potongan sampel yang digunakan untuk melatih model individu,
* criterion, fungsi untuk mebgukur kualitasi pemisahan (*split*)

Dengan Grid Search, diperoleh parameter terbaik:
* n_estimators = 150,
* learning_rate = 0.1,
* loss = squared_error,
* subsample = 0.5,
* criterion = friedman_mse
"""

from sklearn.ensemble import GradientBoostingRegressor

model4 = GradientBoostingRegressor()
parameters4 = {
    'n_estimators' : [25, 50, 100, 150, 200],
    'learning_rate' : [0.01, 0.05, 0.1, 0.5, 1],
    'loss' : ['squared_error', 'absolute_error', 'huber', 'quantile'],
    'subsample' : [0.1, 0.5, 1],
    'criterion' : ['friedman_mse', 'squared_error', 'mse']
}

gradboost_grid = GridSearchCV(model4, parameters4, cv = 5)

gradboost_grid.fit(X_train, y_train)

gradboost_grid.best_params_

gradboost_grid.best_score_

gradboosting = GradientBoostingRegressor(learning_rate=0.1, loss='squared_error', n_estimators = 150, random_state=42, subsample = 0.5, criterion = 'friedman_mse')                             
gradboosting.fit(X_train, y_train)
models.loc['train_r2','GradBoost'] = r2_score(y_pred=gradboosting.predict(X_train), y_true=y_train)

"""### Training Comparison

Dari nilai R<sup>2</sup> proses latih, dapat diketahui bahwa model Random Forest memiliki skor tertinggi sehingga layak dipilih menjadi solusi. Di sini, Random Forest memiliki R<sup>2</sup> = 0,97.
"""

models

"""## Evaluation

Sebelum melakukan evaluasi, data uji akan dikenakan scaling terlebih dahulu.
"""

X_test.loc[:, X_test.columns.to_list()] = scaler.transform(X_test[X_test.columns.to_list()])

model_dict = {
    'SVM': svr, 
    'RandomForest': RF, 
    'AdaBoost': adaboosting, 
    'GradBoost': gradboosting
}

for name, model in model_dict.items():
  models.loc['test_r2', name] = r2_score(y_true=y_test, y_pred=model.predict(X_test))

models

models = models.T

fig, ax = plt.subplots()
models.sort_values(by='test_r2', ascending=False).plot(kind='barh', ax=ax, zorder=3)
ax.grid(zorder=0)
plt.savefig('Model_Comparison.png')

idx = np.random.choice(list(range(345)))

prediction = pd.DataFrame(X_test.iloc[idx, :]).T.copy()
pred_dict = {'y_true' : y_test.iloc[idx]}
for name, model in model_dict.items():
    pred_dict['prediksi_'+name] = model.predict(prediction).round(1)
 
pd.DataFrame(pred_dict)

"""Seperti telah disebutkan sebelumnya, metrik yang digunakan untuk mengukur kinerja model prediksi adalah nilai **R<sup>2</sup>**. Nilai ini diperoleh dengan mengikuti persamaan:

$$ R^2 = 1 - {SSE \over SST} $$  <br>
$$ SSE = \sum (y_{true} - y_{pred})^2 $$ <br>
$$ SST = \sum (y_{true} - \bar{y}_{true})^2 $$ <br>

Dari nilai R<sup>2</sup>, model dapat dibagi menjadi tiga:
1.   Model yang akurat, yaitu apabila nilai R<sup>2</sup> mendekati 1.0
2.   Model biasa, yaitu apabila nilai R<sup>2</sup> di sekitar 0.0
3.   Model buruk, yaitu yaitu nilai R<sup>2</sup> kurang dari 0.0

Dari proses latih dan evaluasi, dapat diketahui bahwa model Random Forest memiliki nilai R<sup>2</sup> yang mendekati satu sehingga dapat dikatakan sebagai model prediksi yang akurat. Random Forest memiliki nilai R<sup>2</sup> latih dan uji masing-masing sebesar 0,97 dan 0,81. Dengan begitu, model ini dapat dipilih untuk melakukan prediksi energi yang dihasilkan PLTS dalam kurun waktu tertentu.

Untuk membuktikan bahwa model Random Forest dapat memenuhi tujuan proyek, dilakukan prediksi terhadap data acak pada data uji. Di sini, untuk nilai energi 5769,63 kWh, model Random Forest memprediksi dengan angka 5503,1 kWh. Nilai prediksi yang tidak terlalu jauh dari nilai sesungguhnya.
"""