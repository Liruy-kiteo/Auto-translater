import customtkinter as ctk
from PIL import Image

class TopLevelSettings():
    '''
    Класс определяет окно настроек, его функции и логику, чтобы подключить его потом к основному приложению
    '''
    def __init__(self):
        """
        создаёт главное окно
        """
        #----------------объявление второго окна настроек(вызывать только когда надо)----------------------------------
        self.settings=ctk.CTkToplevel()
        self.settings.geometry('400x600')
        self.settings.title('Настройки')

        #-----------------------------------создание поля Canvas-------------------------------------------------------
        self.canvas_settings = ctk.CTkCanvas(self.settings, bg='#000000', width=400, height=600,highlightthickness=0)
        self.canvas_settings.pack(anchor='center')

        #---------------------------------------проверка переменных языка и цвета текста-------------------------------
        #проверка, записывает все переменные если они уже есть(чтобы обозначить выбранные на данный момент настройки в приложении)
        try:
         #открывает файл настроек
         with open('settings.txt','r+') as file:
                  self.data_settings = file.readlines()
         #записывает переменные цвета текста и языки
         self.language = self.data_settings[0]
         self.text_color = self.data_settings[1]
        #если не получилось, создаёт свои переменные для цвета текста и языка
        except:
         self.language = 'eng'
         self.text_color = '#ffffff'
         print(self.language)

        #проверяет цвет текста, чтобы не записывать его хеш кодом, для пользователя так будет удобнее(пока только 2 цвета, белый и фиолетовый)
        if self.text_color == '#ffffff' or self.text_color == '#FFFFFF':
             self.color_name = 'Белый'
        else:
             self.color_name = 'Фиолетовый'

        #----------------------------------------Создание кнопок и надписей--------------------------------------------

        #данные для расставления кнопок
        self.button_data = [(340,30,100,40,'Английский',lambda :self.change_language('eng')),(340,80,100,40,'Японский',lambda :self.change_language('jpn')),
                            (340,200,100,40,'Белый',lambda :self.change_color('#FFFFFF')),(340,250,100,40,'Фиолетовый',lambda :self.change_color('#9900FF')),(200,550,360,50,'Подтвердить',self.write_logs)]
        
        #создание всех кнопок в приложении
        for x, y, xsize, ysize, text, command in self.button_data:
            self.button = ctk.CTkButton(master=self.settings, text=text, width=xsize, height=ysize, command = command,
                                         fg_color='#000000', border_color='#9900ff',border_width=2, text_color=self.text_color)
            self.canvas_settings.create_window(x,y,window=self.button)

        #создание линии разделяющей настройки
        self.canvas_settings.create_line(1,165,400,165,width=3,fill='#9900ff')

        #данные для расставления текста
        self.text_data = [(150,83,f'Язык на фотографии\nчтобы получить точный перевод\nнужно ставить тот язык\nкоторый будет на фотографии\nсейчас стоит {self.language}'),
                          (140,225,f'цвет текста в приложении\nсейчас стоит {self.color_name}'),(200,480,'Настройки заработают только, \nкогда вы перезапустите приложения')]
        
        #создаёт весь текст в приложении
        for x, y, text in self.text_data:
             self.canvas_settings.create_text(x,y,text=text, fill=self.text_color,font=('Comic Neue','14',))

        #------------------------------------------Важные переменные---------------------------------------------------


    def change_language(self,language):
        '''
        Записывает в переменную язык
        '''
        self.language=language
        #README удаляет последний символ переноса строки ОБЯЗАТЕЛЬНО ОСТАВИТЬ, ИНАЧЕ С КАЖДОЙ ПЕРЕЗАПИСЬЮ ОН НАЧНЁТ ДОБАВЛЯТЬ ДОПОЛНИТЕЛЬНИЙ СИМВОЛ ПЕРЕНОСА СТРОКИ


        

    def change_color(self,color):
        '''
        Записывает в переменную цвет текста
        '''
        self.text_color=color

    def write_logs(self):
        '''
        записывает выбранные язык и цвет текста
        '''
        with open('settings.txt', 'w') as file:
                file.write(self.language + '\n' + self.text_color)
        #уничтожает окно
        self.settings.destroy()

if __name__ == '__main__':
    TopLevelSettings()
