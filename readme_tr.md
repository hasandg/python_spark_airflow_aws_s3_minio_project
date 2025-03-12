# Docker, Spark, Airflow, ve MinIO Kullanarak Veri Analizi


Bu proje, veri analizi iş akışını oluşturmak için Docker, Spark, Airflow ve MinIO teknolojilerini kullanarak güçlü ve
esnek bir çözüm sunuyor. Projenin amacı, veri setini oluşturan iki adet CSV dosyasını MinIO'dan yüklemek, Spark'ı 
kullanarak veri setini analiz etmek ve sonuçları yine MinIO'ya kaydetmektir.

![diagram](./docker_spark_airflow_minio.png)

## 🛠 Kullanılan Teknolojiler ve Metodoloji


1. PySpark kullanılarak Python dilinde bir script yazıldı. Bu script, Airflow scheduler desteği ile 10 dakikada bir verileri MinIO'dan okuyup, Apache Spark kullanarak veri analizi yapar ve sonuçları MinIO'ya kaydeder.
2. Docker ile apache/airflow:2.9.3 base imajı kullanılarak güncel Java ve PySpark kütüphaneleri içeren özel bir Docker imajı oluşturuldu. MinIO erişimi için; AWS'in disk ürünü olan S3 ile uyumlu bağlantı kütüphanesini içeren jar dosyaları da bu imaja eklendi.

3. Proje, aşağıdaki sürümlerle geliştirilmiş ve test edilmiştir:


| Yazılım        | Versiyon     |
|----------------|--------------|
| OpenJDK        | `17.0.2`     |
| Docker         | `25.0.3`     |
| Docker Compose | `2.24.6`     |
| Spark          | `3.5.1`      |
| Hadoop         | `3`          |
| PySpark        | `3.5.1`      |
| Python         | `3.12.4`     |
| Airflow        | `2.9.3`      |
| MinIO          | `2024.7.16`  |


# 🚀 Uygulamanın Çalıştırılması
## 1. Özel Airflow İmajının Oluşturulması

    $ cd python_spark_airflow_aws_s3_minio/src/
    $ docker build --rm -t docker-airflow-custom1:latest .  

## 2. Docker Compose ile Uygulamanın Çalıştırılması
Container'ları başlatmak için:

    $ cd python_spark_airflow_aws_s3_minio/
    $ docker-compose up -d

Çalışma sonrasında container'ları durdurmak için:

    $ docker-compose down


## MinIO Webserver'a verilerin yüklenmesi

[http://localhost:9001](http://localhost:9001)

MinIO webserver'a erişmek için kullanıcı adı ve şifre: 

``` User: minioadmin``` <br> ``` Pass: minioadmin```

MinIO webserver'a erişildikten sonra, `data` adında bir bucket oluşturulmalıdır.
"person_data.csv" ve "country_data.csv" dosyaları bu bucket içine yüklenmelidir.

## Airflow Webserver'a erişim

[http://localhost:8060](http://localhost:8060)

Airflow webserver'a erişmek için kullanıcı adı ve şifre: 

``` User: airflow``` <br> ``` Pass: airflow```

python_spark_airflow_aws_s3_minio/dags klasörüne eklenen dag dosyaları otomatik olarak airflow webserver'da görüntülenecektir.
Bu dosyalar web arayüzünden etkinleştirilerek çalıştırılabilir. Bu arayüzden "data_processing_dag.py" dosyasını etkinleştirerek 
sonuçları MinIO webserver'da bulunan data dizininden kontrol edebilirsiniz.

`python_spark_airflow_aws_s3_minio/dags` klasörüne eklenen DAG dosyaları otomatik olarak Airflow webserver'da görüntülenecektir. 
Bu dosyalar web arayüzünden etkinleştirilerek çalıştırılabilir. Bu arayüzden `data_processing_dag.py` dosyasını etkinleştirerek 
sonuçları MinIO webserver'da bulunan `data` dizininden kontrol edebilirsiniz.

## Erişim Bilgileri 

| Uygulama       | URL                                            | Kullanıcı adı ve şifre                               |
|----------------|------------------------------------------------|------------------------------------------------------|
| Airflow        | [http://localhost:8060](http://localhost:8085) | ``` User: airflow``` <br> ``` Pass: airflow```       |         |
| MinIO          | [http://localhost:9001](http://localhost:9001) | ``` User: minioadmin``` <br> ``` Pass: minioadmin``` |           |
| Postgres       | **Server/Database:** localhost:5432/airflow    | ``` User: airflow``` <br> ``` Pass: airflow```       |           | 