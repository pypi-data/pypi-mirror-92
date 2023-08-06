#!/usr/bin/env python

from kivy.app import App
from kivy.garden.cefpython import CEFBrowser

class Webmin(App):
    def build(self):
        return CEFBrowser(url="https://localhost:10000")
    
    
Webmin().run()