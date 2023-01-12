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

<img src="https://user-images.githubusercontent.com/58902846/208302426-495bf5c1-4bd1-4886-b54e-2fe99b233a17.png" width="500"/><img src="https://user-images.githubusercontent.com/58902846/212163820-187f1865-c526-41cb-963a-a85c8fd49674.JPG" height="220"/>

---

## Introduction/about

For this project I proposed, developed and tested a hardware module based on an Arduino Uno microcontroller and wireless technology via the WebSocket protocol, which measures the openness of Croatian mussels. This information is received by a specially designed application interface that runs on a personal computer connected via a wireless connection.

The build involved designing and planning the components to be used, as well as wiring and soldering everything into a working device. Then the microcontroller is programmed to be able to recive readings from the selected sensors and communicate to the outside.

Idea came from creating connection with constant data transfer between server and microcontroller as client, that's where the name of project "Module for continuous sending" originates from. For it, most fitting comunication protocol appeared as websocket, because of providing full-duplex communication channels over a single TCP connection. After that it got plenty of aditional features like GUI and all actions with it.

It's primary use is to work with analog HALL sensors which are connected to Croatian mussels, givng us complete monitoring of state and measure how open the mussels are. Monitoring of such has plenty of enviromental benefits because mussels react on bad conditions of water, making them ideal bioindicator.

## User interface

| Ver.    |                                                              Main                                                              |                                                             Extras                                                             |
| ------- | :----------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------: |
| Initial | <img src="https://user-images.githubusercontent.com/58902846/208302221-d07cf3a6-0d8e-45bc-8f19-de753a658b27.png" width="450"/> | <img src="https://user-images.githubusercontent.com/58902846/212164473-4c330c9c-b221-43b9-810a-d4a37c34cb86.png" width="220"/> |
| Latest  | <img src="https://user-images.githubusercontent.com/58902846/212116900-90b67e89-89cf-4506-845e-467141c12127.png" width="450"/> | <img src="https://user-images.githubusercontent.com/58902846/212117336-74aac3b0-08d5-414c-ab6f-1662f1c7dd5e.png" width="550"/> |

## Used parts, equipment and services

| #   |                                       Name                                        | Price |
| --- | :-------------------------------------------------------------------------------: | ----: |
| 1   | [Arduino UNO WiFi Rev.2](https://store.arduino.cc/products/arduino-uno-wifi-rev2) |   €45 |
| 1   |                                  UTP cable 20 m                                   |   €25 |
| 6   |                                RJ45 Ethernet Plug                                 |    €2 |
| 2   |                                  Electrical box                                   |    €5 |
| 12  |                         Analog HALL sensors - 49E or 503                          |    €5 |
| 1   |                                 Personal computer                                 |     - |
| 1   |    [Linode Shared CPU](https://www.linode.com/products/shared/) - Nanode 1 GB     | 5$/Mo |
| ... |                                        ...                                        |   ... |

## Current features

- Remote monitoring
- Graphical interface with realtime plotting
- Fully asynchronous websocket connection
- Csv file manager
- **Arduino simulation service**
- **Csv analysis service**

## What's next

- User login and database

## Attachments

1. **[Simplification of connection scheme](https://user-images.githubusercontent.com/58902846/212163308-61c8870c-5e49-4636-b0ab-c81c364dae6a.jpg)**

2. **[Scheme](https://user-images.githubusercontent.com/58902846/212163416-fba7d4a2-5bb2-4c40-90b3-d063e36845c0.jpg)**

---

## Deployed on

```PowerShell
- - Expired subscription - -
```

## Project setup

```PowerShell
python3 -m pip install --user virtualenv

python3 -m venv env

# MAC/Linux
source env/bin/activate
# WIN
.\env\Scripts\activate

# MAC/WIN/Linux
pip3 install requirements
# MAC -> Needed for service
sudo ifconfig lo0 alias 127.0.0.2 up
```

### Project run

```PowerShell
# Start server.py before starting services
python server.py
python services/ArduinoSim.py
python services/AnalyzeCsv.py
```

App should be running on: **[localhost:31310](http://localhost:31310)**
