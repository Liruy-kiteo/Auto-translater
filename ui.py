import customtkinter as ctk
from PIL import Image
from translate_function import Translate
import threading
import time
import os

class UI():
    def __init__(self):

        #---------------Характеристики основного окна-----------------------
        self.root = ctk.CTk()
        self.root.geometry('1000x600')
        self.root.title('АвтоПереводчик')
        self.root.resizable(width=False, height=False)
        self.root.configure(bg='#000000')

        #---------------Создание площади для рисования(Canvas)--------------
        self.canvas = ctk.CTkCanvas(bg='#000000', width=1100, height=700,borderwidth=4, highlightthickness=0)
        self.canvas.pack(anchor='center')

        #----------------функции для отрисовки приложения-------------------
        self.lines_buttons()
        self.root.mainloop() 


    def lines_buttons(self):
        '''
        Отрисовывает главные параметры приложения, линии и кнопки, также задаёт им команды
        '''

        #основные картежи для данных о ui
        self.rectangles_coordinates = [(50, 30, 950, 280), (50, 320, 950, 570)]
        self.buttons_data = [('icons/download.png', 977, 250, 40, self.download_original_text),('icons/author.png', 24, 30, 40, self.placeholder),('icons/download.png', 977, 540, 40, self.download_translated_text),('icons/settings.png', 977, 30, 40, self.placeholder),("icons/copy_photo.png", 480, 170, 60, self.image_place_thread)]

        #цикл итерирует все линии в приложении
        for x1,y1,x2,y2 in self.rectangles_coordinates:
         self.canvas.create_rectangle(x1,y1,x2,y2,outline="#9900ff",width=5)
        
        #цикл итерирует все кнопки в приложении
        for file, x1, y1, xsize, button_command in self.buttons_data:
           self.button_image = ctk.CTkImage(dark_image=Image.open(file),size=(xsize,xsize))
           self.buttons = ctk.CTkButton(master=self.root, image=self.button_image,text='',fg_color='#000000',height=5,width=5,command=button_command)
           self.canvas.create_window(x1,y1,window=self.buttons)

        #просто команда для текста по центру(было бы расточительством тратить её на цикл)
        self.canvas.create_text(495,110,font=('Comic Neue','22',),fill='#9900ff',activefill='#9900ff',text='Скопируйте своё изображение')

    def image_place_thread(self):
       '''
       Запускает отдельный поток для функции image_place
       '''
       
       self.image_thead = threading.Thread(target=self.image_place)
       self.image_thead.start()

    def image_place(self):
       '''
       Функция получает данные о последнем скопированом изображении, дальше отображает в первом блоке изображение, а во втором перевод с текстом
       (перевод отобразится нормлально, только если будет на японском)
       '''
       #флаг состояния, чтобы приложение не копировало много раз одну и туже проверку
       self.previous_image = 0
       #заготавливается виджет текста для переведённого текста из изображения
       self.already_translated_text=ctk.CTkLabel(master=self.root,text='',fg_color='#000000',text_color='#9900ff',font=('Comic Sans',16))
       self.canvas.create_window(500,445,window=self.already_translated_text,anchor='center',width=890, height=240)

       #цикл который бесконечно проверяет наличие изображения, а затем выводит его перевод
       while True:
          #таймер, чтобы проверка не была слишком частой
          time.sleep(3)

          #Если последнии скопированные в буфер обмена данные не являются изображением, то функция начинает всё сначала
          try:
           #берётся изображение из буфера обмена, затем идёт проверка, если оно совпадёт с последним, то дальнейший  код не случится(оптимизация)
           self.img_from_clipboard = Translate.image_grab(self)
           if self.img_from_clipboard != self.previous_image:
            #Возвращается изображение и обрабатывается, дальше вставляется в виджет label чтобы его отобразить
            self.converted_image = ctk.CTkImage(dark_image=self.img_from_clipboard,size=(891,240))
            self.image_first_box = ctk.CTkLabel(master=self.root,image=self.converted_image,width=891,height=240,text='')
            self.canvas.create_window(500,155,window=self.image_first_box)
            #скопированное изображение записывается, чтобы совершить проверку в следующий раз
            self.previous_image = self.img_from_clipboard
            #берётся текст из изображения, затем вставляется в заранее заготовленный виджет
            self.translated_text = Translate.translate_return(self)
            self.already_translated_text.configure(text=self.translated_text)
            #виджет обновляется
            self.already_translated_text.update()

          except:
             continue
          
    #фукнция чтобы заменить некоторые нерабочии кнопки
    def placeholder(self):
       '''
       просто ничего не возвращает
       '''
       return None
    
    def download_translated_text(self):
      '''
      Создаёт и открывает в блокноте весь текст, что был скопирован и переведён
      '''
      try:
        
        #Открывает текстовый файл и записывает его, потом открывает в блокноте
        with open('text.txt', 'w+', encoding='utf-8') as file:
          file.write(self.translated_text)
          os.startfile('text.txt')

      except:
         return None
      
    def download_original_text(self): 
      '''
      Создаёт и открывает в блокноте весь текст, что был скопирован
      '''
      try:
        self.original_text=Translate.original_text(self)
        #Открывает текстовый файл и записывает его, потом открывает в блокноте
        with open('text.txt', 'w+', encoding='utf-8') as file:
          file.write(self.original_text)
          os.startfile('text.txt')

      except:
         return None

if __name__=='__main__':
    UI()

