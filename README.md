# Opis

Ćwiczenia zostały wykonane z pomocą środowiska Python

Do protokołów UDP i TCP została użyta biblioteka `socket`

Do dekodowania i kodowania danych, na format binarny, dla protokołów UDP i TCP została użyta biblioteka `pickle`

Do dekodowania i kodowania danych, na format string, dla protokołów HTTP i MQTT została użyta biblioteka `json`

Do stworzenia serwera HTTP został użyty framework `flask`

Jako broker do protokołu MQTT skorzystałem z publicznie dostępnego pod adresem **test.mosquitto.org**

Link do filmu: https://youtu.be/qMx4Egvvbvg

# Wnioski

- Przy pracy z maszynami wirtualnymi przydaje się dysk współdzielony albo sposób na przesyłanie plików miedzy maszynami (taki jak samba). Ja korzystałem z polecenia `scp` które przesyła pliki przez protokół `ssh`.
- Do pisania serwerów dla różnych protokołów warto jest poszukać frameworków zamiast pisać wszystko od zera. W kodzie użyłem frameworka flask do HTTP, ale również jest dostępny Django. Do UDP i TCP można by było skorzystać z biblioteki  `socketserver`, która implementuje różne rodzaje serwerów na różne sposoby takie jak: w wątkach, asynchronicznie, na różnych rdzeniach procesora (biblioteka `multiprocessing`) itp. Używanie frameworków przydaję się w przypadku gdy serwer ma obsługiwać wielu klientów naraz.
- Każdy z protokołów ma swoje wady i zalety
