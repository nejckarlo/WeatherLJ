'Vreme v Ljubljani'

import json #format shranjevanja podatkov
import urllib.request #spletni standard sprejemanja in oddajanja prošenj

from tkinter import * #GUI modul
from tkinter import ttk #GUI modul

from PIL import ImageTk, Image #slike za GUI
import os


'DODAJ DOSTOP DO VREMENSKIH PODATKOV'
url = 'http://api.openweathermap.org/data/2.5/weather?q=Ljubljana,si&appid=120d38ee8539748e438e1390e2a55ceb'

'definiranje objekta za dostop do podatkov preko HTTP request-a'
response = urllib.request.urlopen(url)

'Podatki so vrnjeni v obliki zakodiranega JSON formata'
result = json.loads(response.read().decode()) #preberemo, nato dekodiramo, zapišemo v spremenljivko

'Pregled vsebine vrnjene vremenske slike'
for kljuc, vrednost in result.items():
    if type(vrednost) == list:
        print('LIST: ' + kljuc, vrednost)
    elif type(vrednost) == dict:
        print('DICT: ' + kljuc, vrednost)
    else:
        print('VAL: ' + kljuc,vrednost)

'DODAJ KODO V OZADJU'

class cityForecast(object):
    def __init__(self, result):
        self.name = result['name'] #ime mesta Ljubljana
        self.weather = result['weather'] #vremenska informacija
        self.wind = result['wind'] #informacija o vetru
        self.sys = result['sys'] #sistemske informacije(vzhod, zahod, ...)
        self.main = result['main'] #temperature, tlak, vlažnost
        self.coords = result['coord'] #koordinate Ljubljane
        self.date = result['dt'] #datum zadnjega merjenja

Ljubljana = cityForecast(result)

def prikaziVreme(args):
    try:
        temperature = args.main['temp']
        pressure = args.main['pressure']
        humidity = args.main['humidity']
        descript = args.weather[0]['description']

        if descript == 'scattered clouds':
            img_id = 'scattered_clouds.png'
        else:
            img_id = 'scattered_clouds.png'

        temp.set(str(temperature-273.15) + ' °C')
        tlak.set(str(pressure) + ' mbar')
        vlaga.set(str(humidity) + ' %')
        img = ImageTk.PhotoImage(Image.open(img_id))
        panel.configure(image = img)
        panel.image = img
    except ValueError:
        print('error')
        pass

'GUI'

root = Toplevel()
root.title('Vreme v Ljubljani') #našemu oknu damo naslov

mainframe = ttk.Frame(root, padding='3 3 12 12') #definiramo glavni okvir in širino praznega prostora znotraj njega
mainframe.grid(column=0, row=0, sticky=(N, W, E, S)) #definiramo mrežo glavnega okvirja in popolnoma raztegnemo
mainframe.columnconfigure(0, weight=1) #definiramo enakomerno raztegljivost vseh stolpcev mreže
mainframe.rowconfigure(0, weight=1) #definiramo enakomerno raztegljivost vseh vrstic mreže

temp = StringVar()
tlak = StringVar()
vlaga = StringVar()
image = PhotoImage()

'Definiranje teksta'
ttk.Label(mainframe, text='Trenutno vreme').grid(column=2, row=1, sticky=W)
ttk.Label(mainframe, text='Temperatura').grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text='Zračni tlak').grid(column=1, row=3, sticky=E)
ttk.Label(mainframe, text='Zračna vlažnost').grid(column=1, row=4, sticky=E)

'Definiranje tekstovnih spremenljivk'
ttk.Label(mainframe, textvariable=temp).grid(column=2, row=2, sticky=(W, E))
ttk.Label(mainframe, textvariable=tlak).grid(column=2, row=3, sticky=(W, E))
ttk.Label(mainframe, textvariable=vlaga).grid(column=2, row=4, sticky=(W, E))

'POMEMBNO'
'       command-lambda: prikaziVreme(Ljubljana)'
'       dodamo lambda, da tipka "ostane ne pritisnjena" ko zaženemo program in tipka čaka na pritik uporabnika'
ttk.Button(mainframe, text='Vreme Ljubljana', command=lambda: prikaziVreme(Ljubljana)).grid(column=1, row=5, sticky=W)

img = ImageTk.PhotoImage(Image.open('Lj-logo.png'))
panel = ttk.Label(mainframe, image = img)
panel.grid(column=3, row=2, rowspan=3, sticky=E)

root.bind('<Return>', prikaziVreme)
root.mainloop()
