# по сути библиотеки, чтобы забрать изображение и перевести его в текст
from PIL import Image, ImageGrab
import pytesseract
from deep_translator import GoogleTranslator

#класс определяет главную функцию(перевод с картинки)
class Translate():
    def translate_return(self, language_on_image):

     #дальнейший код сработает только в том случае если в clipboard последним файлом было сохранено изображение

     try:
      #берет последнее изображение из clipboard
      self.img = ImageGrab.grabclipboard()

      #переводит изображение в формат который читает tesseract, нужен для того чтобы pytesseract мог работать с alt+prtsc
      #из-за того что он сохраняет данные в bitmap(если не ошибаюсь), а не png
      self.text_from_img = self.img.convert("RGB")

      #переводит изображение в текст
      self.text = pytesseract.image_to_string(self.text_from_img, lang=f"{language_on_image}") 

      #переводит текст на русский, определяет его автоматически(по сути обращается в google translate, как request, но проще)
      translator = GoogleTranslator(source='auto', target='ru')
      result = translator.translate(self.text)

      #возвращает перевод текста в картинке
      return result
     except:
      return None
     #если в clipboard не было изображения, то функция выдаёт ошибку ValueError

    
    def image_grab(self):
      '''
      Функция возвращает последний сохранённый в clipboard файл, если это изображение
      Если это не изображение, то функция возвращает None
      '''
      try:
       return ImageGrab.grabclipboard()
      except:
       return None
      
    def original_text(self, language_on_image):
      '''
      Функция возвращает исходный текст с изображения
      '''
      #дальнейший код сработает только в том случае если в clipboard последним файлом было сохранено изображение
      try:
      
       #берет последнее изобра ение из clipboard, 
       self.img = ImageGrab.grabclipboard()

       #переводит изображение в формат который читает tesseract, нужен для того чтобы pytesseract мог работать с alt+prtsc
       #из-за того что он сохраняет данные в bitmap(если не ошибаюсь), а не png
       self.text_from_img = self.img.convert("RGB")

       #переводит изображение в текст
       self.text = pytesseract.image_to_string(self.text_from_img, lang=f'{language_on_image}') 

       #возвращает текст в картинке
       return self.text
     
      #если в clipboard не было изображения, то функция выдаёт ошибку ValueError
      except:
       return ValueError
      
if __name__ == '__main__':
   Translate()

