from selenium import webdriver
from components.base import Base

def before_scenario(context, scenario):
    context.browser = webdriver.Chrome()
    context.base = Base(context.browser)

def after_scenario(context, scenario):
    context.browser.quit()