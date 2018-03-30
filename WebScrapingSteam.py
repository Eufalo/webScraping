import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog,QMessageBox,QTableWidgetItem,QWidget,QHeaderView
from PyQt5 import uic
from PyQt5 import QtCore
import os
class Juego():
  
    def __init__(self,nombre,descr,idiom,plataforma,precio,precio_desc,areciente,tanalisis,valoracionM,url):
        self.descr=descr
        self.nombre=nombre
        self.idiom=idiom
        self.plataforma=plataforma
        self.precio=precio
        self.precio_desc=precio_desc
        self.areciente=areciente
        self.tanalisis=tanalisis
        self.valoracionM=valoracionM
        self.url=url
class Ventana_Principal(QMainWindow):
 #Método constructor de la clase
 def __init__(self):
  #Iniciar el objeto QMainWindow
  QMainWindow.__init__(self)
  #Cargar la configuración del archivo .ui en el objeto
  uic.loadUi("WebScrapingMainWindow.ui", self)   
  self.nam_categorias=[]
  self.index_categorias=[]
  self.juegos=[]
  self.nam_categorias,self.index_categorias=categorias_tags()
 def cellClick(self,row,col):
     
     urljuegos=[]
     
     page=1
     while(len(urljuegos)<50 and page<4):
         for i in urls(self.index_categorias[row],page):
            if(len(urljuegos)<50): 
             urljuegos.append(i)
         page=page+1
     e=0
     for i in urljuegos:
         
         self.textBrowser.setText(i)
         self.textBrowser.repaint()
         self.juegos.append(info_Juego(i))
         e=e+1
         self.progressBar.setValue(e)
         self.progressBar.repaint()
     self.con_tabla_Juegos()
     create_excell(self.juegos,self.nam_categorias[row])
     QMessageBox.about(self, "¡Busqueda completada!", "Excell Creado ")
 def con_tabla_Juegos(self):
      
      #añadirle las cabeceras
      header = ["Nombre","Descripcion","Precio","URL"]
      #cargamos la tabla de violencia
      self.table_Juegos.setColumnCount(4)
      aux=self.juegos
      self.table_Juegos.setHorizontalHeaderLabels(header)
      self.table_Juegos.setRowCount(5)
      #Añadimos el controlador
      #self.table_Categorias.cellClicked.connect(self.cellClick)
      r=0
      for i in aux[0],aux[1],aux[2],aux[3],aux[4]:
        c=0  
        for e in range(4):
            if c==0:
                item=QTableWidgetItem(aux[r].nombre)
            else:
                if c==1:
                    item=QTableWidgetItem(aux[r].descr) 
                else:
                    if c==2:
                        item=QTableWidgetItem(aux[r].precio)
                    else:
                        if c==3:
                            item=QTableWidgetItem(aux[r].url)
            item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
            self.table_Juegos.setItem(r,c,item )
            c=c+1
        r=r+1
      head = self.table_Juegos.horizontalHeader()
      head.setSectionResizeMode(QHeaderView.Stretch)
      head.setStretchLastSection(True) 
      self.table_Juegos.repaint()
    #cargamos la tabla de genericas
 def con_tabla(self):
      
      #añadirle las cabeceras
      header = ["Categoria"]
      #cargamos la tabla de violencia
      self.table_Categorias.setColumnCount(1)
      aux=self.nam_categorias
      self.table_Categorias.setHorizontalHeaderLabels(header)
      self.table_Categorias.setRowCount(len(aux))
      #Añadimos el controlador
      self.table_Categorias.cellClicked.connect(self.cellClick)
      r=0
      
      for i in aux:
        c=0  
        item=QTableWidgetItem(i)
        item.setFlags( QtCore.Qt.ItemIsSelectable |  QtCore.Qt.ItemIsEnabled )
        self.table_Categorias.setItem(r,c, item)
        r=r+1
      head = self.table_Categorias.horizontalHeader()
      head.setSectionResizeMode(QHeaderView.Stretch)
      head.setStretchLastSection(True)  
    #cargamos la tabla de genericas
def precion_change(xl,juego,tag):
    nuevo_precio=[]
    cells={'Precio +Reciente':[],'Precio viejo':[],'Nombre':[]}
    if(len(xl.sheet_names)>1):
        df1 = xl.parse(xl.sheet_names[1])
    #if((df1.Nombre!=None) and (df1.Precio!=None):
        for i, r in enumerate(df1.Nombre):
            for e in juego:
                if(r==e.nombre):
                    if(df1.Precio[i]!=e.precio):
                        nuevo_precio.append(e.precio)
                    else :
                        nuevo_precio.append('~')
        cells['Precio +Reciente']=nuevo_precio
        cells['Precio viejo']=df1.Precio
        cells['Nombre']=df1.Nombre
    
        df = pd.DataFrame(cells)
        writer = pd.ExcelWriter('.'+os.path.sep+'Excell'+os.path.sep+tag+'_Actualizacion_Precios.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name=xl.sheet_names[1])
                        
def create_excell(juegos,tag):
    descr=[]
    nombre=[]
    idiom=[]
    plataforma=[]
    precio=[]
    precio_desc=[]
    areciente=[]
    tanalisis=[]
    valoracionM=[]
    url=[]
    cells={'Nombre':[],'URL':[],'Descripcion':[],'Idioma':[],'Plataforma':[],'Precio':[],
           'Preecio con Descuento':[],'Analisis recinete':[],'Analisis Total':[],'Analisis Metacritic':[]}
    if(os.path.exists('.'+os.path.sep+'Excell'+os.path.sep+tag+'.xlsx')):
        xl = pd.ExcelFile('.'+os.path.sep+'Excell'+os.path.sep+tag+'.xlsx')
        if(xl!=None):
            precion_change(xl,juegos,tag)
        
    for i in juegos:
       descr.append(i.descr)
       nombre.append(i.nombre)
       idiom.append(i.idiom)
       plataforma.append(i.plataforma)
       precio.append(i.precio)
       precio_desc.append(i.precio_desc)
       areciente.append(i.areciente)
       tanalisis.append(i.tanalisis)
       valoracionM.append(i.valoracionM)
       url.append(i.url)
    cells['Nombre']=nombre
    cells['URL']=url
    cells['Descripcion']=descr
    cells['Idioma']=idiom
    cells['Plataforma']=plataforma
    cells['Precio']=precio
    cells['Preecio con Descuento']=precio_desc
    cells['Analisis recinete']=areciente
    cells['Analisis Total']=tanalisis
    cells['Analisis Metacritic']=valoracionM
    df = pd.DataFrame(cells)
    writer = pd.ExcelWriter('.'+os.path.sep+'Excell'+os.path.sep+tag+'.xlsx', engine='xlsxwriter')
    if(os.path.exists('.'+os.path.sep+'Excell'+os.path.sep+tag+'.xlsx')):
        xl = pd.ExcelFile('.'+os.path.sep+'Excell'+os.path.sep+tag+'.xlsx')
        df.to_excel(writer, sheet_name=xl.sheet_names[0])
    else:
        df.to_excel(writer, sheet_name='Sheet1')
    '''
    worksheet.conditional_format('B2:B49', {'type': 'data_bar'})
    worksheet.conditional_format('D2:D49', {'type': 'data_bar'})
    '''
    
def urls(tag,page):
    urljuegos=[]
    #Dependiendo la categoria que seleccione el usuario dispondremos de una url u otra
    url_pagina_tag="http://store.steampowered.com/search/?sort_by=Reviews_DESC&tags="+str(tag)+"&page="+str(page)       
    page_juegos_categorias=requests.get(url_pagina_tag)
    soup2 =BeautifulSoup(page_juegos_categorias.content,'html.parser')
    urls_juego=soup2.find_all("a",class_="search_result_row")
    for url in urls_juego:
        #if(len(urljuegos)<50):
            if "/app/" in url.attrs['href']:
                urljuegos.append(url.attrs['href'])
    return urljuegos
def categorias_tags():
    pagina = requests.get("http://store.steampowered.com/search/?sort_by=Reviews_DESC")
    soup =BeautifulSoup(pagina.content,'html.parser')
    html=soup.find_all('div', class_='tab_filter_control')
    n=0
    categorias=[]
    htmlreference=[]
    while(n<379):
        categorias.append(html[n].get_text().strip())
        htmlreference.append(html[n]['data-value'])
        n=n+1
    return categorias,htmlreference
def analisis_juego(url_juego,nombre):
    '''
    STEAM:
        
    Analisis recientes areciente-> El % de los  análisis de los usuarios en los últimos 30 días.
																			
    Todos los analisis tanalisis-> El % de los  análisis de los usuarios sobre este juego.
																							
    
    METACRITIC:
        
    valoracionM
    '''
    areciente=""
    tanalisis=""
    valoracionM=""
    cookies={'birthtime':'283993201','mature_content':'1'}
    pagina = requests.get(url_juego,cookies=cookies)
    soup =BeautifulSoup(pagina.content,'html.parser')
    '''
    anal_reciente=soup.find_all('div',class_='user_reviews_summary_row')
    
    if(len(anal_reciente)>1):
        aux1=anal_reciente[0].get_text()
        aux1=re.split(r'%', aux1)
        areciente=aux1[0]
        aux2=anal_reciente[1].get_text()
        aux2=re.split(r'%', aux2)
        tanalisis=aux2[0]
        areciente=re.split(r'-',areciente)
        areciente=areciente[1]
        tanalisis=tanalisis[1]
    else :
        if(len(anal_reciente)==1):
            aux2=anal_reciente[0].get_text()
            aux2=re.split(r'%', aux2)
            tanalisis=aux2[0]
            tanalisis=re.split(r'-',tanalisis) 
            tanalisis=tanalisis[1]
    '''
    anal_reciente=soup.find_all('span',class_='game_review_summary')
 
      
    if(len(anal_reciente)>3):
        aux1=anal_reciente[3]['data-store-tooltip']
        aux1=re.split(r'%', aux1)
        areciente=aux1[0]
        aux2=anal_reciente[2]['data-store-tooltip']
        aux2=re.split(r'%', aux2)
        tanalisis=aux2[0]
    
    
    else :
        if(len(anal_reciente)==2):
            aux2=anal_reciente[1]['data-store-tooltip']
            aux2=re.split(r'%', aux2)
            tanalisis=aux2[0]
        
    meta=soup.find('div',class_='score high')
    if(meta!=None):#Si encuentra la valoracion de metacritic
        valoracionM=meta.get_text()
        valoracionM=valoracionM.strip()
    #areciente.strip(),tanalisis.strip()
      
    
    return areciente,tanalisis,valoracionM     
    
def plata(p):
    if (p=="Windows"):
        return "Windows"
    else:  
        if (p=="Mac"):
            return "Mac"
        else:  
            if (p=="Linux"):
                return "Linux"
    return ''
def info_Juego(url_juego):
    '''
    arryifo->nombre,descr,idiom,plataforma,precio,precio_desc
    Nombre
    Precio
    Idioma
    Descripcion
    Plataforma
    '''
    cookies={'birthtime':'283993201','mature_content':'1'}
    pagina = requests.get(url_juego,cookies=cookies)
    soup =BeautifulSoup(pagina.content,'html.parser')
    descr=''
    nombre=''
    idiom=[]
    plataforma=[]
    precio=''
    precio_desc=''
    
    #NOMBRE
    nombre=soup.find('div',class_='apphub_AppName').get_text() 
    #ANALISIS
    areciente,tanalisis,valoracionM=analisis_juego(url_juego,nombre)
    #PRECIO
    prec=soup.find('div', class_='game_purchase_action').get_text()
    prec=list(re.split(r'[\n\t\r ]', prec))
    i=0;
    aux=''
    while (aux==''):
        if(prec[i]!=''):
            aux=prec[i]
        i=i+1
    aux=list(re.split(r'%', aux))
    if(len(aux)==1):#si no tiene precio con descuento 
        precio=aux[0]
       
        
    else:
        if(len(aux)>1):#si tiene precio con descuento
             aux1=list(re.split(r'€',aux[1]))# separamos el precio del decuento
             precio=aux1[0]
             precio_desc=aux1[1]
    
    #DESCRIPCION         
    descripcion=soup.find('div', class_='game_description_snippet')
    if(descripcion!=None):
        descr=descripcion.get_text().strip()
    else:
        descr=''
    #IDIOMA
    idiomas=soup.find('table', class_='game_language_options').get_text()
    idiomas = list(re.split(r'[\n\t\r ]', idiomas))
    for i in idiomas:
        if (i=="Spanish"):
            idiom.append("Español")
        else:  
            if (i=="English"):
                idiom.append("Ingles")
    #PLATAFORMA
    platform=soup.find('div', class_='sysreq_tabs')
    if(platform!=None):#Comprobamos si exite una tabla donde se encuentran los idiomas
        platform=platform.get_text()
        platform= list(re.split(r'[\n\t\r ]', platform))
        for p in platform:
            aux=plata(p)
            if(aux!=''):
                plataforma.append(aux)
            
    else:#Si no se encuentra la tabla solo abri un idioma 
        platform=soup.find('div', class_='game_area_sys_req_rightCol')#Al solo haber un idioma elegimos la version Recomendada
        if(platform!=None):
            platform=platform.get_text()
            platform= list(re.split(r'[\n\t\r ]', platform))
            for p in platform:
                aux=plata(p)
                if(aux!=''):
                    plataforma.append(aux)
    if(len(plataforma)==0):
        plataforma.append("Windows")
    jueg=Juego(nombre,descr,idiom,plataforma,precio,precio_desc,areciente,tanalisis,valoracionM,url_juego)           
    #return nombre,descr,idiom,plataforma,precio,precio_desc,areciente,tanalisis,valoracionM
    return jueg
'''
urljuegos=[]
juegos=[]
page=1;
tag=19;


#print (categorias)
#print(htmlreference)
#Url de la pagina principal de steam para poder sacar los tags de las categorias que esta pagina dispone
url_pagina_sintags="http://store.steampowered.com/search/?sort_by=Reviews_DESC"

page_juegos_categorias=requests.get("http://store.steampowered.com/search/?sort_by=Reviews_DESC&tags=19&page=0")
while(len(urljuegos)<50):
    urljuegos=urls(tag,page)
    page=page+1

for i in urljuegos:
    print("URL " , i)
    juegos.append(info_Juego(i))

create_excell(juegos,categoria)
'''
#Instancia para iniciar una aplicación
app = QApplication(sys.argv)
#Crear un objeto de la clase
_ventana = Ventana_Principal()
#Mostra la ventanaç
_ventana.con_tabla()
_ventana.show()
#Ejecutar la aplicación
app.exec_()
'''
print(categorias_tags())   
analisis_juego(urljuegos[1])
'''
