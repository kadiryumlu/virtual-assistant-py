from datetime import datetime
import webbrowser

def getCurrentTime():
    return datetime.now().strftime('%H:%M')

def getTodaysWeather(lacation):
    return ''

def searchInGoogle(keywords):
    url = f'https://www.google.com/search?q={keywords}'
    webbrowser.get().open_new_tab(url)

