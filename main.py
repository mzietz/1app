#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kivy
import json
import os
from os.path import join, exists
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.label import Label
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.properties import ListProperty, NumericProperty
from operator import itemgetter, attrgetter
from jsonlibrary import Library
from kivy.base import EventLoop

from kivy.animation import Animation
from kivy.clock import Clock

class SwipeManager(ScreenManager):
    pass

class PageOne(Screen):
    picture = StringProperty("data/pictures/anleitung.png")
    picture_opacity = NumericProperty(1)

class PageTwo(Screen):
    pass

class FinishedPage(Screen):
    picture = StringProperty("data/pictures/homescreen.png")
    # def on_enter(self):
    #     animation = Animation(duration=.5)
    #     animation = Animation(pos_hint_y = 1, t='in_out_cubic', duration=.2)
    #     animation.start(self.ids.complete)
class VocabFrontPage(Screen):
    picture = StringProperty("data/pictures/homescreen.png")
    deck = StringProperty("")
    level = StringProperty("")

class HomePage(Screen):
    picture = StringProperty("data/pictures/homescreen.png")
    # first_time = True
    # def on_enter(self):
    #     if self.first_time:
    #         Clock.schedule_once(self.animate, timeout=1.2)
    #         self.first_time = False
    #     else:
    #         Clock.schedule_once(self.animate)
    # def animate(self, dt):
    #     for x in [self.ids.study_button, self.ids.settings_button, self.ids.data_button]:
    #         animation = Animation(duration=.5)
    #         animation = Animation(y=x.y+10, t='in_out_cubic', duration=.2)
    #         animation += Animation(y=x.y-10, t='out_bounce', duration=.3)
    #         animation.start(x)

class ChunkPage(Screen):
    picture = StringProperty("data/pictures/homescreen.png")
    deck = StringProperty("")
    level = StringProperty("")

class AboutPage(Screen):
    picture = StringProperty("data/pictures/aboutdesign.png")

class DataPage(Screen):
    picture = StringProperty("data/pictures/homescreen.png")
    a1_image = StringProperty("data/pictures/A1.png")
    a2_image = StringProperty("data/pictures/A2.png")
    b1_image = StringProperty("data/pictures/B1.png")
    b2_image = StringProperty("data/pictures/B2.png")

    nomen_image = StringProperty("data/pictures/deck_hallo_raw.png")
    verben_image = StringProperty("data/pictures/deck_hallo_raw.png")
    adjektive_image = StringProperty("data/pictures/deck_hallo_raw.png")
    rest_image = StringProperty("data/pictures/deck_hallo_raw.png")  

class OneApp(App):
    vocab1 = StringProperty()
    vocab2 = StringProperty()
    answer1 = StringProperty()
    answer2 = StringProperty()
    info11 = StringProperty()
    info12 = StringProperty()
    info21 = StringProperty()
    info22 = StringProperty()
    current_deck = StringProperty()
    swipe_left = NumericProperty()
    swipe_right = NumericProperty()
    
    def build(self):
        kivy.Config.set('graphics', 'width',  380)
        kivy.Config.set('graphics', 'height', 610)
        self.title = 'Swiper'
        self.sm = SwipeManager()
        self.sm.transition = SlideTransition(duration=.4, direction='left')
        self.homepage = HomePage(name = 'home')
        self.vocabfrontpage = VocabFrontPage(name = 'vocabfrontpage')
        self.datapage = DataPage(name = 'datapage')
        self.chunkpage = ChunkPage(name = 'chunkpage')
        self.pageone = PageOne(name ='pageone')
        self.pagetwo = PageTwo(name ='pagetwo')
        self.aboutpage = AboutPage(name ='aboutpage')
        self.finishedpage = FinishedPage(name ='finishedpage')
        self.sm.add_widget(self.homepage)
        self.sm.add_widget(self.aboutpage)
        self.sm.add_widget(self.datapage)
        self.sm.add_widget(self.vocabfrontpage)
        self.sm.add_widget(self.chunkpage)
        self.sm.add_widget(self.finishedpage)
        self.sm.add_widget(self.pageone)
        self.sm.add_widget(self.pagetwo)
        self.sm.current = 'home'
        self.lib = Library()
        self.lib.load_decks()
        self.set_current_deck()
        self.lib.load_vocabs()
        self.load_intro()
        self.swipe_left, self.swipe_right = self.lib.swipe_value()
        return self.sm

    def init(self):
        self.lib.current_chunk = self.lib.next_chunk()
        self.lib.reset_learned_status()
        self.lib.next_card()
        self.vocab1 = self.lib.library[self.lib.current_card]["question"]
        self.answer1 = ""
        self.info11 = ""
        self.info12 = ""
        self.vocab2 = self.lib.library[self.lib.current_card]["question"]
        self.answer2 = ""
        self.info21 = ""
        self.info22 = ""
        self.answered = False

    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.sm.transition.direction = 'left'
            self.go_to_home()
            return True 

    def go_to_vocabfrontpage(self):
        self.sm.transition.direction = 'left'
        self.swipe_left, self.swipe_right = self.lib.swipe_value()
        self.lib.load_vocabs()
        self.init()
        self.sm.current = 'vocabfrontpage'
        
    def set_current_deck(self):
        for x in self.lib.decks:
            if x["selected"] == True:
                self.current_deck = x["text"]
                self.currentLevel = x["text"][:2]
                self.lib.current_deck = x["text"]
                self.reset_level_pictures()
                self.choose_level_pictures(x["text"][:2])
                self.choose_deck_pictures(x["text"][2:])
                self.set_deck_and_level_images("settingspage", x["text"][:2],x["text"][2:])
        self.lib.save_decks()

    def go_to_data(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'datapage'

    def go_to_vocab(self):
        self.sm.transition.direction = 'left'
        self.lib.load_vocabs()
        self.init()
        if self.lib.finished:
            self.sm.current = 'finishedpage'
        else:
            self.sm.current = 'pageone'

    def go_to_chunkpage(self):
        self.sm.transition.direction = 'left'
        self.lib.save_vocabs()
        self.lib.save_decks()
        self.swipe_left, self.swipe_right = self.lib.swipe_value()
        self.sm.current = 'chunkpage'

    def go_to_home(self):
        self.sm.transition.direction = 'right'
        self.sm.current = 'home'

    def go_to_about(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'aboutpage'

    def go_to_one(self, direction):
        self.answered = False
        if self.lib.cards_left() == 1 and direction == 'left':
            self.lib.add_swipe('right')
            self.go_to_chunkpage()
        else:   
            if direction == 'left':
                self.lib.i_know_card()
            elif direction == 'right':
                self.lib.i_dont_know_card()
            self.lib.next_card()
            self.vocab1 = self.lib.library[self.lib.current_card]["question"]
            self.answer1 = ""
            self.info11 = ""
            self.info12 = ""
            self.sm.transition.direction = direction
            self.sm.current = 'pageone'

    def go_to_two(self, direction):
        self.answered = False
        if self.lib.cards_left() == 1 and direction == 'left':
            self.lib.add_swipe('right')
            self.go_to_chunkpage()
        else:
            if direction == 'left':
                self.lib.i_know_card()
            elif direction == 'right':
                self.lib.i_dont_know_card()
            self.lib.next_card()
            self.vocab2 = self.lib.library[self.lib.current_card]["question"]
            self.answer2 = ""
            self.info21 = ""
            self.info22 = ""
            self.sm.transition.direction = direction
            self.sm.current = 'pagetwo'
    
    def load_intro(self):
        if self.lib.firsttime:
            self.pageone.picture_opacity = 1
        else:
            self.pageone.picture_opacity = 0
        self.lib.firsttime = False
        self.lib.save_decks()

    def show_answer(self, screen):
        if screen == self.pageone:
            self.answer1 = self.lib.library[self.lib.current_card]["answer"]
            self.info11 = self.lib.library[self.lib.current_card]["info1"]
            self.info12 = self.lib.library[self.lib.current_card]["info2"]
        elif screen == self.pagetwo:
            self.answer2 = self.lib.library[self.lib.current_card]["answer"]
            self.info21 = self.lib.library[self.lib.current_card]["info1"]
            self.info22 = self.lib.library[self.lib.current_card]["info2"]

    def touchdown(self, touch):
        self.coordinate = touch.x   

    def reset_current_deck(self):
        self.lib.reset_deck()

    def touchup_on_pagetwo(self, touch):
        self.distance = touch.x - self.coordinate       
        if self.answered == False:
            self.show_answer(self.pagetwo)
            self.answered = True
        else:
            if self.distance > 50:
                self.go_to_one('right')
            elif self.distance < -50:
                self.go_to_one('left')

    def touchup_on_pageone(self, touch):
        try:
            self.distance = touch.x - self.coordinate
        except:
            pass
        if self.pageone.picture_opacity != 0:
            self.pageone.picture_opacity = 0    
        else:
            if self.answered == False:
                self.show_answer(self.pageone)
                self.answered = True
            else:
                if self.distance > 50:
                    self.go_to_two('right')
                elif self.distance < -50:
                    self.go_to_two('left')  

    def on_level_button(self, level):
        self.reset_level_pictures()
        self.choose_level_pictures(level)
    
    def reset_deck_pictures(self):
        self.datapage.nomen_image = "data/pictures/deck_hallo_raw.png"
        self.datapage.verben_image = "data/pictures/deck_hallo_raw.png"
        self.datapage.adjektive_image = "data/pictures/deck_hallo_raw.png"
        self.datapage.rest_image = "data/pictures/deck_hallo_raw.png"

    def reset_level_pictures(self):
        self.datapage.a1_image = "data/pictures/A1.png"
        self.datapage.a2_image = "data/pictures/A2.png"
        self.datapage.b1_image = "data/pictures/B1.png"
        self.datapage.b2_image = "data/pictures/B2.png"
    
    def choose_deck_pictures(self, deck):
        if deck == "nomen":
            self.datapage.nomen_image = "data/pictures/nomen.png"
        if deck == "verben":
            self.datapage.verben_image = "data/pictures/verben.png"     
        if deck == "adjektive":
            self.datapage.adjektive_image = "data/pictures/adjektive.png"       
        if deck == "rest":
            self.datapage.rest_image = "data/pictures/rest.png"

    def choose_level_pictures(self, level):
        if level == "a1":
            self.currentLevel = "a1"
            self.datapage.a1_image = "data/pictures/A1gross.png"
            self.reset_deck_pictures()
        if level == "a2":
            self.currentLevel = "a2"
            self.datapage.a2_image = "data/pictures/A2gross.png"    
            self.reset_deck_pictures()    
        if level == "b1":
            self.currentLevel = "b1"
            self.datapage.b1_image = "data/pictures/B1gross.png"    
            self.reset_deck_pictures()    
        if level == "b2":
            self.currentLevel = "b2"
            self.datapage.b2_image = "data/pictures/B2gross.png"
            self.reset_deck_pictures()
    
    def on_deck_button(self, deck):
        self.current_deck = self.currentLevel + deck
        self.lib.current_deck = self.current_deck
        self.lib.save_decks()
        self.set_current_deck()
        self.reset_deck_pictures()
        self.choose_deck_pictures(deck)

    def set_deck_and_level_images(self, page, level, deck):
        if deck == "nomen":
            self.vocabfrontpage.deck = "명사"
            self.chunkpage.deck = "명사"
        if deck == "verben":
            self.vocabfrontpage.deck = "동사"     
            self.chunkpage.deck = "동사"
        if deck == "adjektive":
            self.vocabfrontpage.deck = "형용사"      
            self.chunkpage.deck = "형용사"
        if deck == "rest":
            self.vocabfrontpage.deck = "나머지"
            self.chunkpage.deck = "나머지"
        if level == "a1":
            self.vocabfrontpage.level = "A1"
            self.chunkpage.level = "A1"
        if level == "a2":
            self.vocabfrontpage.level = "A2"    
            self.chunkpage.level = "A2"    
        if level == "b1":
            self.vocabfrontpage.level = "B1"    
            self.chunkpage.level = "B1"    
        if level == "b2":
            self.vocabfrontpage.level = "B2"
            self.chunkpage.level = "B2"

    # def click_animate(self, instance):
    #     # animation = Animation(size_hint_x = instance.size_hint_x - .05, duration=.01)
    #     animation = Animation(size_hint_y = instance.size_hint_y - .05, duration=.01)
    #     # animation += Animation(size_hint_x = instance.size_hint_x + .05, duration=.2)
    #     animation += Animation(size_hint_y = instance.size_hint_y + .05, duration=.2)
    #     animation.start(instance)
    #     # animation = Animation(size_hint_x = instance.size_hint_x - .001, duration=.1)
    #     # animation &= Animation(size_hint_y = instance.size_hint_y - .001, duration=.1)
    #     # animation.start(instance)

if __name__ == '__main__':
    OneApp().run()