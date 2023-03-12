from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
import speech_recognition as sr
from deep_translator import GoogleTranslator
import random
import os
from gtts import gTTS
import time
from datetime import datetime
import os.path
from kivy.uix.togglebutton import ToggleButton

final_text, prefix, translated_text = '', '', ''



def record_audio():
    r = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        #print("Audio Starting")
        #print("Start Talking ^_^")
        audio = r.listen(source)
        #for x in range(0, random.randint(2, 100)):
        #    print('........')
        #print("Speaking Time Ended")
    return audio

def speech_to_text(speech, engine = 'google+standard', alternate=False):
    r = sr.Recognizer()
    
    if(engine == 'google+standard'):
        return r.recognize_google(speech, show_all=False)
    elif(engine == 'wit.ai+standard'):
        if not alternate:
            return r.recognize_wit(audio_data=speech, show_all=False, key='WSZRTAK5LBEEXNFPXZYBDY5V7Z7KXECN')
        else:
            return r.recognize_wit(audio_data=speech, show_all=True, key='WSZRTAK5LBEEXNFPXZYBDY5V7Z7KXECN')

def translate_text(pre=None, text=None):
    return GoogleTranslator(source='auto', target=pre).translate(text)



class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)



class ChoiceWindow(Screen):
        def __init__(self, **kwargs):
            super(ChoiceWindow, self).__init__(**kwargs)
            self.btn2 = Button(text='Microphone')
            #self.add_widget(self.btn2)
            self.btn3 = Button(text='Recording')
            #self.add_widget(self.btn3)
            self.btn4 = Button(text='Text')
            #self.add_widget(self.btn4)
            self.btn2.bind(on_press = self.screen_transition_mic)
            self.btn3.bind(on_press = self.screen_transition_record)
            self.btn4.bind(on_press = self.screen_transition_text)
            
            self.box_layout = BoxLayout()
            self.box_layout.add_widget(self.btn2)
            self.box_layout.add_widget(self.btn3)
            self.box_layout.add_widget(self.btn4)
            self.add_widget(self.box_layout)

        def screen_transition_text(self, *args):
            self.manager.current = 'text'

        def screen_transition_mic(self, *args):
            self.manager.current = 'mic'

        def screen_transition_record(self, *args):
            self.manager.current = 'record'

class TextWindow(Screen):
    def __init__(self, **kwargs):
            super(TextWindow, self).__init__(**kwargs)

            self.btn2 = Button(text='Submit')
            self.textinput = TextInput(text='', multiline=True)

            self.btn2.bind(on_press = self.save_text)

            self.box_layout = BoxLayout()
            self.box_layout.add_widget(self.btn2)
            self.box_layout.add_widget(self.textinput)
            self.add_widget(self.box_layout)

    def screen_transition_result(self, *args):
        self.manager.current = 'language_choice'

    def save_text(self, *args):
        global final_text
        final_text = self.textinput.text
        self.screen_transition_result()

class MicWindow(Screen):
    def __init__(self, **kwargs):
            super(MicWindow, self).__init__(**kwargs)

            self.mic = sr.Microphone()
            
            self.btn2 = Button(text='Click To Start Recording')

            self.label_text = TextInput(text='Click the button, wait 2 seconds, and speaking.', font_size='20sp', multiline=True)
            
            self.box_layout = BoxLayout()
            self.box_layout.add_widget(self.btn2)
            self.box_layout.add_widget(self.label_text)

            self.btn2.bind(on_press = self.record_and_update)
            
            self.add_widget(self.box_layout)

            
    def record_and_update(self, *args):
        global final_text
        
        captured_audio = record_audio()
        actual_text = speech_to_text(speech = captured_audio, engine = 'wit.ai+standard')
        final_text = actual_text
        
        
        self.btn3 = Button(text='Continue', pos=(0,0), size_hint=(.3,.3))
        self.box_layout.add_widget(self.btn3)
        #self.label_text.text = actual_text + '\n \n \n' + '--------------------- \n' + 'Is this is text you desired? If yes, then press the continue button. Otherwise re-record the message or click on and manually edit the text. DO NOT alter any text after the line.'
        self.label_text.text = actual_text
        
    def screen_transition_result(self, *args):       
        self.manager.current = 'language_choice'



        #with open("ROM_text.txt", "w+") as file:
        #    file.write('----')
        
        #os.startfile('audio_recorder.py')

        #while True:
        #    with open("ROM_text.txt", "r+") as file:
        #        f = file.readline().strip()
        #    if f != '----':
        #        break
        #with open("ROM_text.txt", "r+") as file:
        #    f = file.read()
        #    self.label_text.text = f

class RecordWindow(Screen):
    def __init__(self, **kwargs):
        super(RecordWindow, self).__init__(**kwargs)

class LanguageChoiceWindow(Screen):
    def __init__(self, **kwargs):
        super(LanguageChoiceWindow, self).__init__(**kwargs)
        self.list_of_langs = [('German', 'de'), ('Spanish', 'es'), ('French', 'fr'), ('Chinese(S)', 'zh-CN'), ('Chinese(T)', 'zh-TW'), ('Japanese', 'ja'), ('Korean', 'ko'), ('Arabic', 'ar'), ('Hebrew', 'iw'), ('Hindi', 'hi'), ('Urdu', 'ur')]
        self.dict_of_langs = dict(self.list_of_langs)
        self.btn_list = []

        for x,y in self.list_of_langs:
            curr_btn = Button(text=x)
            curr_btn.bind(state = self.get_choice)
            self.btn_list.append(curr_btn)
            

        self.box_layout = BoxLayout()

        for x in self.btn_list:
            self.box_layout.add_widget(x)

        self.add_widget(self.box_layout)


    def get_choice(self, instance, value):
        global prefix, final_text, translated_text
        
        prefix = self.dict_of_langs.get(instance.text)
        
        translated_text = translate_text(pre=prefix, text=final_text)
        
        self.screen_transition_result()

    def screen_transition_result(self, *args):       
        self.manager.current = 'view_lang'

class LanguageViewWindow(Screen):
    def __init__(self, **kwargs):
        super(LanguageViewWindow, self).__init__(**kwargs)

        self.curr_btn = Button(text='CLICK TO VIEW TRANSLATED TEXT')
        self.curr_btn.bind(on_press=self.display_text)

        self.box_layout = BoxLayout()
        
        self.box_layout.add_widget(self.curr_btn)

        self.add_widget(self.box_layout)

    def display_text(self, *args):
        global translated_text

        self.box_layout.remove_widget(self.curr_btn)

        self.txt = TextInput(text=translated_text, font_name='arial-unicode-ms.ttf')
        
        self.box_layout.add_widget(self.txt)

        self.btn3 = Button(text='Continue', pos=(0,0), size_hint=(.3,.3))
        
        self.btn3.bind(on_press = self.screen_transition_audioScreen)

        self.box_layout.add_widget(self.btn3)

    def screen_transition_audioScreen(self, *args):       
        self.manager.current = 'audio'

class AudioWindow(Screen):
    def __init__(self, **kwargs):
        super(AudioWindow, self).__init__(**kwargs)

        self.btn2 = Button(text='Enter a filename for your audio clip \n and then press this button')
        self.textinput = TextInput(text='', multiline=False)

        self.btn2.bind(on_press = self.save_play_audio)

        self.box_layout = BoxLayout()
        self.box_layout.add_widget(self.btn2)
        self.box_layout.add_widget(self.textinput)
        self.add_widget(self.box_layout)

        
    def save_play_audio(self, *args):
        global translated_text, prefix

        self.speechObj = gTTS(text=translated_text, lang=prefix)
        self.speechObj.save(self.textinput.text+'.mp3')

        #with open("records.txt", "a") as file:
        #    file.write('\n'+'Audio File Name => '+ filename+'.mp3')

        os.system(self.textinput.text+'.mp3')

        time.sleep(3)
        exit()

class Application(App):
    def build(self):
        sm = ScreenManagement(transition=FadeTransition())
        sm.add_widget(ChoiceWindow(name='choice'))
        sm.add_widget(TextWindow(name='text'))
        sm.add_widget(MicWindow(name='mic'))
        sm.add_widget(RecordWindow(name='record'))
        sm.add_widget(LanguageChoiceWindow(name='language_choice'))
        sm.add_widget(LanguageViewWindow(name='view_lang'))
        sm.add_widget(AudioWindow(name='audio'))
        return sm


if __name__ == "__main__":
    Application().run()
