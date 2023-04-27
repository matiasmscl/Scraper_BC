import scrapy
import time

class BC0(scrapy.Spider):
    name = 'BC0'
    start_urls = ["https://bdemovil.bcentral.cl/"]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0)',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'BC0.json'
    }
    def parse(self, response):
        self.log('__________________________________________________________')
        self.log('Visitamos: '+response.url)
        if response.url == "https://bdemovil.bcentral.cl/":
            contenedor=scrapy.Selector(response).css('div[id="collapseThree"]')
            print(contenedor)
            for cont in contenedor:
                Elemento=cont.css('div>ul>li>a::text').extract()
                Pagina=cont.css('div>ul>li>a::attr(href)').extract()
                for k in range(0,len(Pagina)):
                    siguiente=Pagina[k]
                    time.sleep(1)
                    print('siguiente: '+str(siguiente))
                    yield response.follow(siguiente, self.parse)
        else:
            contenedor=scrapy.Selector(response).css('div[class="row"]')
            for cont in contenedor:
                Elemento=cont.css('h4>a::text').extract_first()
                Pagina=cont.css('h4>a::attr(href)').extract_first()
                yield{'Grupo':response.url,'Elemento':Elemento,'Pagina':Pagina}


