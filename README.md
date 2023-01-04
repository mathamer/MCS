# MCS

Application name:
**Module for continuous sending**

Faculty of informatics pula:
https://fipu.unipu.hr/

\
<img src="https://user-images.githubusercontent.com/58902846/210407981-928df4c7-1f6f-4d16-8d06-f4a017fa4a62.png" width="450"/>

\
Kolegij:
**[Web aplikacije](https://www.notion.so/Web-aplikacije-7ba8350d498546a78812399024edac44) i [Raspodjeljeni sustavi](https://fiputreca.notion.site/fiputreca/Raspodijeljeni-sustavi-544564d5cc9e48b3a38d4143216e5dd6)**

Note:
Izrađeno za kolegij web aplikacije kao projekt te primijenjeno u svrhe završnog rada pod nazivom
“Izrada ugradbenog računalnog sustava za praćenje filtriranja školjkaša pomoću hall senzora“. Trenutačno nastavljen development u sklopu kolegija raspodjeljeni sustavi.

Ak.god. **2020/21**  
Nastavnik i mentor: doc. dr. sc. **[Nikola Tanković](https://www.notion.so/Kontakt-stranica-875574d1b92248b1a8e90dae52cd29a9)**  
Demonstrator: **Nikki Bernobić**, bacc. inf.

Ak.god. **2022/23**  
Nastavnik i mentor: doc. dr. sc. **[Nikola Tanković](https://www.notion.so/Kontakt-stranica-875574d1b92248b1a8e90dae52cd29a9)**  
Asistent: **Srđan Daniel Simić**, mag. inf.

### Izlagano **25.-27.11.2022.** na sajmu [CROFISH](https://www.crofish.eu/) u Poreču 🐟

<img src="https://user-images.githubusercontent.com/58902846/208302426-495bf5c1-4bd1-4886-b54e-2fe99b233a17.png" width="500"/>

## User interface

![MCS_webapps](https://user-images.githubusercontent.com/58902846/208302221-d07cf3a6-0d8e-45bc-8f19-de753a658b27.png)

## Used parts and equipment

| #   |                                       Name                                        | Price |
| --- | :-------------------------------------------------------------------------------: | ----: |
| 1   | [Arduino UNO WiFi Rev.2](https://store.arduino.cc/products/arduino-uno-wifi-rev2) |   €45 |
| 1   |                                  UTP cable 20 m                                   |   €25 |
| 12  |                                Analog HALL sensors                                |    €2 |
| 1   |                                 Personal computer                                 |     - |
| ... |                                        ...                                        |   ... |

## Current features

- Remote monitoring
- Graphical interface with realtime plotting
- Fully asynchronous websocket connection
- Csv file manager
- Arduino simulation service
- Csv analysis service

## What's next

- User login and database

---

## Deployed on

```
- - Expired subscription - -
```

## Project setup

```
MAC/WIN
pip3 install requirements
MAC
sudo ifconfig lo0 alias 127.0.0.2 up
# Needed for service
```

### Project run

```
python server.py
python services/ArduinoSim.py
python services/AnalyzeCsv.py
```
