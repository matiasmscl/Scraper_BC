import pandas
import scrapy

#####################Funcion
class BC1(scrapy.Spider):
    Matriz=pandas.read_json('BC0.json')
    Matriz=Matriz.dropna(subset=['Elemento','Grupo','Pagina'])
    for k in Matriz.index:
        if Matriz.at[k,'Elemento']==[] or Matriz.at[k,'Grupo']==[] or Matriz.at[k,'Pagina']==[]:
            Matriz=Matriz.drop(k)
        else:
            Matriz.at[k,'Codigo']=str(Matriz.at[k,'Pagina']).split('/BDE/Series/')[1].split('?')[0]
    Matriz.to_csv('IndicadoresBC.csv',sep='|')
    tx=[]
    for k in Matriz.index:
        tx=tx+['https://si3.bcentral.cl/bdemovil/BDE/SeriesData/'+Matriz.at[k,'Codigo']]
    for k in range(0,len(tx)):
        print(tx[k])
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'BC1.json'
    }
    name = 'BC1'
    start_urls = tx
    def parse(self, response):
        self.log('__________________________________________________________')
        self.log('Visitamos: '+response.url)
        k=0
        titulo=str(response.url).split('/SeriesData/')[1]
        aux=response.css('td::text')
        while k < len(aux):
            filaTabla = aux[k:k+2].extract()
            fecha= filaTabla[0]
            Valor= filaTabla[1]
            #if filaTabla[1].find('.')>0: Valor=','.join(Valor.split('.'))
            #if filaTabla[1].find(',')>0: Valor='.'.join(Valor.split(','))
            yield{'Titulo':titulo,'Fecha':fecha,'Valor':Valor}
            k=k+2
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'+titulo)
