#!/usr/bin/env python

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from cefpython3 import CEFBrowser

Builder.load_string('''
<Webmin>:
    orientation: 'vertical'
    Label:
        text: 'Server'
    Input:
        text: 'localhost'
        on_text: root.server = args[1]
    Label:
        text: 'Port'
    Input:
        text: '10000'
        on_text: root.port = args[1]
    Button:
        text: 'Connect'
        on_press: root.connect()
''')


class Webmin(App):
    server = 'localhost'
    port = '10000'
    def connect(self):
        return CEFBrowser(url="https://"+server+":"+port)
    def build(self):
        return connect()
    
    
Webmin().run()