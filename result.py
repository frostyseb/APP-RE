import kivy
import requests
import json
import urllib.request
import app_page

from kivy.app import App
from kivy.uix.button import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.core.window import Window
from functools import partial
from app_page import AppPage

kivy.require("2.0.0")
