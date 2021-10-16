from time import sleep
import telebot
from ast import literal_eval
import mss
import pyautogui as pyg
import cv2
from telebot import types
import os
import numpy
 
 
bot = telebot.TeleBot('1234567890:ABCDEEEEEEEEEEE') #токен бота
 
issense = False #дефолт настройка режима сенсорного ввода
 
@bot.message_handler(content_types=["text", "sticker", "pinned_message", "photo", "audio"])
def get_text_messages(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add('/mon',"дабл-клик")
 
    if message.text == "дабл-клик" or message.text == "/mon" or message.text == "/help" or message.text == "/sens" or message.text == "/sensoff" or message.text == "левее" or message.text == "правее" or message.text == "ниже" or message.text == "выше" or message.text == "нажать":
        global issense
      
        if message.text == "дабл-клик":
            pyg.doubleClick()
      
        if message.text == "выше":
            pyg.move(0, -100)
      
        if message.text == "ниже":
            pyg.move(0, 100)
      
        if message.text == "левее":
            pyg.move(-100, 0)
      
        if message.text == "правее":
            pyg.move(100, 0)
      
        if message.text == "нажать":
            pyg.click()
      
        if message.text == "/sens":
            issense = True
            bot.send_message(message.from_user.id, "режим сенсорного ввода) чтобы отключить /sensoff", reply_markup=types.ReplyKeyboardRemove())
      
        if message.text == "/sensoff":
            issense = False
            bot.send_message(message.from_user.id, "режим сенсорного ввода отключен епты", reply_markup=markup)
 
        if message.text == "/help":
            bot.send_message(message.from_user.id, """
/mon - показать монитор
/sens - режим сенсорного ввода
/sensoff - выйти из режима сенсорного ввода""")
          
        if message.text != "/help":
            if not issense:
                with mss.mss() as sct:
                    currentMouseX, currentMouseY = pyg.position()
                    filename = sct.shot(mon=1, output="mon.png")
                image = cv2.imread('mon.png')
                cv2.circle(image, (currentMouseX, currentMouseY), 10, (0,0,255), -1)
                cv2.imwrite("mon.png", image)
                photo = open('mon.png', 'rb')
                markup
                markup.add('левее','правее','выше','ниже', 'нажать')
                bot.send_photo(message.from_user.id, photo, reply_markup=markup)
 
            if issense:
                with mss.mss() as sct:
                    currentMouseX, currentMouseY = pyg.position()
                    filename = sct.shot(mon=1, output="mon.png")
                image = cv2.imread('mon.png')
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cv2.imwrite("mon.png", gray_image)
                photo = open('mon.png', 'rb')
                bot.send_photo(message.from_user.id, photo, reply_markup=markup)
 
    elif message.content_type == 'photo': #если пришло фото от пользователя
        photo_id = message.photo[-1].file_id
        file_photo = bot.get_file(photo_id)
        filename, file_extension = os.path.splitext(file_photo.file_path)
        downloaded_file_photo = bot.download_file(file_photo.file_path)
        src = 'photos/' + photo_id + file_extension
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file_photo)
        nameoflastphoto = str(photo_id + file_extension)
        if issense:
            try:
                imagerz = cv2.imread(str('photos/' + str(nameoflastphoto)))
                imgfindgray = numpy.array(imagerz)
                hsv_min = numpy.array((1, 80, 80), numpy.uint8)
                hsv_max = numpy.array((20,250,250), numpy.uint8)
                hsv = cv2.cvtColor(imgfindgray, cv2.COLOR_BGR2HSV)
                thresh = cv2.inRange(hsv, hsv_min, hsv_max)
                moments = cv2.moments(thresh, 1)
                dM01 = moments['m01']
                dM10 = moments['m10']
                dArea = moments['m00']
                x = int(dM10 / dArea)
                y = int(dM01 / dArea)
                pyg.click(x * 1.5, y * 1.5)
                currentMouseX, currentMouseY = pyg.position()
              
                os.remove('photos/' + str(nameoflastphoto))
                with mss.mss() as sct:
                    sleep(0.2)
                    currentMouseX, currentMouseY = pyg.position()
                    filename = sct.shot(mon=1, output="mon.png")
                  
                image = cv2.imread('mon.png')
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cv2.imwrite("mon.png", gray_image)
                photo = open('mon.png', 'rb')
                bot.send_photo(message.from_user.id, photo, reply_markup=markup)
            except:
                bot.send_message(message.from_user.id, "ошибка, чтоб использовать сенсорный режим нарисуйте точку на фотографии")
                os.remove('photos/' + str(nameoflastphoto))
        elif not issense:
            bot.send_message(message.from_user.id, """чтобы включить режим сенсорного ввода
/sens""")
            os.remove('photos/' + str(nameoflastphoto))
          
    else:
      try:
            pyg.move(literal_eval(message.text))
            with mss.mss() as sct:
                    currentMouseX, currentMouseY = pyg.position()
                    filename = sct.shot(mon=1, output="mon.png")
            image = cv2.imread('mon.png')
            cv2.circle(image, (currentMouseX, currentMouseY), 10, (0,0,255), -1)
            cv2.imwrite("mon.png", image)
            photo = open('mon.png', 'rb')
            markup
            markup.add('левее','правее','выше','ниже', 'нажать')
            bot.send_photo(message.from_user.id, photo, reply_markup=markup)
      except:
          bot.send_message(message.from_user.id, """
/mon - показать монитор
/sens - режим сенсорного ввода
/sensoff - выйти из режима сенсорного ввода""")
 
bot.polling(none_stop=True)
