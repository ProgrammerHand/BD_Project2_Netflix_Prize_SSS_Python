# BD_Project2_Netflix_Prize_SSS_Python run instructio

## Wstęp
W razie jakichkolwiek pytań bardzo zalecam skontaktować się

Discord: bonbons1
Facebook: Dima Optiman (https://www.facebook.com/dima.optiman/)

## Wgrywanie danych
Zanim zaczniemy uruchamiać wszystko potrzebujemy dannych z jakimi będziemy pracować. Żeby nie wgrywać ich ręcznie na cluster wgramy ich do gcs po czym będziemy kopiować na cluster.
Na początku wchodzimy w zakladke "Cloud Storage-> Buckets"

image

Tutaj zjeżdżamy na dól i musimy już mieć stworzony bucket ( w ramach rodzialu "Utworzenie zasobnika (bucket)" z instrukcji "Konfiguracja środowiska zajęć - część 3 - zapoznanie się ze środowiskiem GCP: Storage, Dataproc")

image

Na przykladzie on ma nazwe "pbds-24-dp", może być inna nazwa ale wtedy będziemy musieli zmieniać plik konfiguracyjny.
Klikamy na nazwe bucket'a i trafiamy do jego structury

image

Tutaj za pomocy przycisków "Upload files"(dla "movie_titles.csv") oraz "Upload Folder" (dla folderu "netflix-prize-data") wgrywamy dane
Gdy w strukturze pojawili się wspomniany plik i folder wiemy że dane zostali zaladowane

image

## Przygotowanie srodowiska
Urachamiamy cluster wpisując do consoli polecenie

```shell
gcloud dataproc clusters create ${CLUSTER_NAME} \
--enable-component-gateway --bucket ${BUCKET_NAME} --region ${REGION} --subnet default \
--master-machine-type n1-standard-4 --master-boot-disk-size 50 \
--num-workers 2 --worker-machine-type n1-standard-2 --worker-boot-disk-size 50 \
--image-version 2.1-debian11 --optional-components DOCKER,ZOOKEEPER \
--project ${PROJECT_ID} --max-age=2h \
--metadata "run-on-master=true" \
--initialization-actions \
gs://goog-dataproc-initialization-actions-${REGION}/kafka/kafka.sh
```
Po uruchomieniu otwieramy w nowej kartce polączenie ssh
Sciągamy projekt z publicznego repozytorium i rozpakowujemy z folderu
```shell
git clone https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python.git
mv BD_Project2_Netflix_Prize_SSS_Python/* .
```
![image](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/dd1192b4-7db3-4bf8-b534-894c89d50b22)

Gdy uzywamy bucket'u innego niz ww to musimy wyedytowac plik z wartosciami parametrów srodowiska

``` shell
nano env_params.sh
```
Zmieniamy wartość BUCKET_NAME wpisując nazwe używanego bucket'u, zapisujemy i wychodzimy (Ctrl + s, Ctrl + x)
![image](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/515f6f0f-bc8e-42e3-a27d-e8bf8050eff8)
Po wykonaniu lub pominiencie poprzedniego kroku przygotowujemy środowisko
``` shell
source ./env_setup.sh
```
![image](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/62a52387-f806-451b-870f-bfa686e939ab)


# Uruchamianie aplikacji
Zeby uruchomić aplikacje musimy uruchomić konsumenta\ów, silnik przetwarzający dane oraz producenta w oddzielnych terminalach ssh
Uruchamiamy konsumenta dannych rzeczywistych
``` shell
source ./realtime_database_consumer.sh
```
Gdy w terminalu zacząl pojawiać się komunikat "Added Data" możemy powiedzieć że konsument dziala
Następnie uruchamiamy konsumenta danych surowych
```
source ./raw_input_consumer.sh
```
Tutaj czekamy na komunikat "Subscribed to topic: ____ with bootstrap server ___"


Teraz uruchamiamy silnik
``` shell
source ./sss_engine.sh
```
Pomijając dużą ilość warning'ów patrzymy czy pojawil się komunikat o schemacie dannych oraz czy pojawiają się komunikaty jak na obrazie poniżej

image

Gdy tak to wiemy że silnik dziala
Zostalo tylko urychomić producenta
``` shell
source ./kafka_producer.sh
```

## Wyniki
Gdy wszystko uruchomilo się to musimy zacząć otrzymywać wyniki

konsument surowych danych

image

konsument bazy dannych

image

Dodatkowo możemy polączyć się z bazą ręcznie
```shell
psql -h localhost -p 8432 -U postgres
```
I sprawdzić ręcznie
```
\c 
```






