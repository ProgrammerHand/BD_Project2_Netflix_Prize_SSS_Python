# BD_Project2_Netflix_Prize_SSS_Python run instructio

## Wstęp
W razie jakichkolwiek pytań bardzo zalecam skontaktować się

Discord: bonbons1
Facebook: Dima Optiman (https://www.facebook.com/dima.optiman/)

## Wgrywanie danych
Zanim zaczniemy uruchamiać wszystko potrzebujemy dannych z jakimi będziemy pracować. Żeby nie wgrywać ich ręcznie na cluster wgramy ich do gcs po czym będziemy kopiować na cluster.
Na początku wchodzimy w zakladke "Cloud Storage-> Buckets"
![Screenshot (114)_1](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/6e692fb9-39b0-4978-a176-2acacbac1bfe)
Tutaj zjeżdżamy na dól i musimy już mieć stworzony bucket ( w ramach rodzialu "Utworzenie zasobnika (bucket)" z instrukcji "Konfiguracja środowiska zajęć - część 3 - zapoznanie się ze środowiskiem GCP: Storage, Dataproc")
![image](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/45a8d3d8-f179-4ac2-9d45-dd65e1ab5db7)
Na przykladzie on ma nazwe "pbds-24-dp", może być inna nazwa ale wtedy będziemy musieli zmieniać plik konfiguracyjny.
Klikamy na nazwe bucket'a i trafiamy do jego structury
![Screenshot (116)_1](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/9b754091-b9d2-48f3-8fbe-b4dc5f9bcf35)
Tutaj za pomocy przycisków "Upload files"(dla "movie_titles.csv") oraz "Upload Folder" (dla folderu "netflix-prize-data") wgrywamy dane(Uwaga przy wgrywaniu folderu nie whodziemy wewnątrz niego, a tylko wybieramy)
![image](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/430da662-a6ad-4222-9965-3dfe9cbc579c)
![Screenshot (116)_2](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/b5d883da-4296-455e-b6d5-2d5084d3a27d)
Gdy w strukturze pojawili się wspomniany plik i folder wiemy że dane zostali zaladowane
![image](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/c4d4c1bc-5581-4d06-b848-2905b941c5ea)
![image](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/b1dda180-1296-4428-93e3-c156b77426c0)
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
![image](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/dd44933a-c429-4461-82f7-89058561e69b)
Następnie uruchamiamy konsumenta danych surowych
```
source ./raw_input_consumer.sh
```
Tutaj czekamy na komunikat "Subscribed to topic: ____ with bootstrap server ___"
![image](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/c725d918-9c59-4be4-b9e2-bcdc96b543c7)
Teraz uruchamiamy silnik
``` shell
source ./sss_engine.sh
```
Pomijając dużą ilość warning'ów patrzymy czy pojawil się komunikat o schemacie dannych
![image](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/d8c2b217-c176-44af-90eb-f9cde794ac1e)
I czy czy pojawiają się komunikaty jak na obrazie poniżej
![image](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/654fdb9f-6422-4a85-9813-572faee41348)
Gdy tak to wiemy że silnik dziala
Zostalo tylko urychomić producenta
``` shell
source ./kafka_producer.sh
```
Gdy zostali wypisane parametry to producent zacząl dzialać
![image](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/de0e856c-b1c9-4f5f-af12-ce150ddf964f)
## Wyniki
Gdy wszystko uruchomilo się to musimy zacząć otrzymywać wyniki

konsument surowych danych
![image](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/7ba6ad4b-92e8-471b-8786-f21fe655139b)
konsument bazy dannych
![image](https://github.com/ProgrammerHand/BD_Project2_Netflix_Prize_SSS_Python/assets/73993616/862b9fb7-e182-461b-9452-193f2f2a2ede)
Dodatkowo możemy polączyć się z bazą ręcznie
```shell
export PGPASSWORD='mysecretpassword'
psql -h localhost -p 8432 -U postgres
```
I sprawdzić ręcznie
```
\c netflix_prize_data
select * from film_scores order by window_start;
```



