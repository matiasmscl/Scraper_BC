import time
start_time = time.time()
import pandas
import os
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

if os.path.exists('BC0.json'):
    os.remove('BC0.json')
if os.path.exists('BC1.json'):
    os.remove('BC1.json')

from BC0 import BC0
configure_logging()
runner = CrawlerRunner()
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(BC0)
    time.sleep(10)
    from BC1 import BC1
    yield runner.crawl(BC1)
    time.sleep(1)
    reactor.stop()
crawl()
reactor.run()

###Ajuste de la informacion:
time.sleep(10)
Matriz=pandas.read_json('BC1.json')
print(Matriz.index)

if os.path.exists('BC_Anual.csv'):
    MatrizAnual=pandas.read_csv('BC_Anual.csv',sep='|')
    MatrizAnual=MatrizAnual.set_index('Fecha')
else:
    MatrizAnual=pandas.DataFrame()
if os.path.exists('BC_Trimestral.csv'):
    MatrizTrimestral=pandas.read_csv('BC_Trimestral.csv',sep='|')
    MatrizTrimestral=MatrizTrimestral.set_index('Fecha')
else:
    MatrizTrimestral=pandas.DataFrame()
if os.path.exists('BC_Mensual.csv'):
    MatrizMensual=pandas.read_csv('BC_Mensual.csv',sep='|')
    MatrizMensual=MatrizMensual.set_index('Fecha')
else:
    MatrizMensual=pandas.DataFrame()
if os.path.exists('BC_Diaria.csv'):
    MatrizDiaria=pandas.read_csv('BC_Diaria.csv',sep='|')
    MatrizDiaria=MatrizDiaria.set_index('Fecha')
else:
    MatrizDiaria=pandas.DataFrame()

meses={'ene':'01','feb':'02','mar':'03','abr':'04','may':'05','jun':'06','jul':'07','ago':'08','sep':'09','oct':'10','nov':'11','dic':'12'}

for k in Matriz.index:
    Aux=Matriz.at[k,'Fecha'].split('-')
    if len(Aux)==1:
        Aux1=pandas.to_datetime(Aux[0]).year
        MatrizAnual.at[Aux1,Matriz.at[k,'Titulo']]=Matriz.at[k,'Valor']
    if len(Aux)==2:
        if Aux[0].find('T')>=0:
            MatrizTrimestral.at[str(Aux[1])+'-'+str(Aux[0]),Matriz.at[k,'Titulo']]=Matriz.at[k,'Valor']
        else:
            MatrizMensual.at[str(Aux[1])+'-'+meses[str(Aux[0])],Matriz.at[k,'Titulo']]=Matriz.at[k,'Valor']
    if len(Aux)==3:
            MatrizDiaria.at[str(Aux[2])+'-'+meses[str(Aux[1])]+'-'+str(Aux[0]),Matriz.at[k,'Titulo']]=Matriz.at[k,'Valor']

print(Matriz)
MatrizAnual=MatrizAnual.sort_index(ascending=True)
MatrizAnual.index.name='Fecha'
print(MatrizAnual)

MatrizTrimestral=MatrizTrimestral.sort_index(ascending=True)
MatrizTrimestral.index.name='Fecha'
print(MatrizTrimestral)

MatrizMensual=MatrizMensual.sort_index(ascending=True)
MatrizMensual.index.name='Fecha'
print(MatrizMensual)

MatrizDiaria=MatrizDiaria.sort_index(ascending=True)
MatrizDiaria.index.name='Fecha'
print(MatrizDiaria)

MatrizAnual.to_csv('BC_Anual.csv',sep='|')
MatrizTrimestral.to_csv('BC_Trimestral.csv',sep='|')
MatrizMensual.to_csv('BC_Mensual.csv',sep='|')
MatrizDiaria.to_csv('BC_Diaria.csv',sep='|')

print("--- %s seconds ---" % (time.time() - start_time))

