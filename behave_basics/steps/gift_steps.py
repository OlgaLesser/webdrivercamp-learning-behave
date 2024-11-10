from time import sleep
from behave import *
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import re


@step('Print the current url')
def step_impl(context):
    print(context.browser.current_url)

@step('Navigate to {url}')
def step_impl(context, url):
    context.browser.get(url)
    context.execute_steps('When Print the current url')

@step('Search for {search_item}')
def step_impl(context, search_item):
    locator = '//*[@id="search"]'
    context.base.send_keys(locator, search_item)
    sleep(5)
    context.base.wait_for_page_load(5)

@step('Verify header of the page contains {expected_text}')
def step_impl(context, expected_text):
    header_element = context.browser.find_element(By.XPATH, "//h1[@data-test='page-title']")
    actual_text = header_element.text
    print("Header found: "+ actual_text)
    assert expected_text == actual_text, f"Header text does not contain '{expected_text}'"

@step('Select {option} in {section} section')
def step_impl(context, option, section):
    locator = (By.XPATH, f"//div[@data-test='@web/SlingshotComponents/Browse' and descendant::span[text() = '{section}']]//span[text() ='{option}']")
    context.base.click(locator)

@step('Collect all items on the first page into {var}')
@step('Collect all items on the first page into {var} on the {level} level')
def step_impl(context, var, level=None):
    items = []
    sleep(3)
    item_elements = context.browser.find_elements(By.XPATH, "//div[@data-test='@web/ProductCard/body']")
    for item_element in item_elements:
        item_data = {
            "title": item_element.find_element(By.XPATH, ".//a[@data-test='product-title']").text,
            "price": item_element.find_element(By.XPATH, ".//span[@data-test='current-price']/span").text,
        }
        try:
            shipment_text = item_element.find_element(By.XPATH, ".//span[@data-test='LPFulfillmentSectionShippingFA_standardShippingMessage']/span[@class='h-text-greenDark']").text
            item_data["shipment_text"] = shipment_text
        except NoSuchElementException:
            pass
        items.append(item_data)
    setattr(context.feature, var, items)

@step('Verify all collected results\' {param} is {condition}')
def step_impl(context, param, condition):
    if param == 'price':
        price_cond = int(condition.split()[1])
        for item in context.feature.collected_items:
            price = extract_number(item['price'])
            assert price < price_cond , f"Price is higher than '{price_cond}'"
            print('Verify price finished')
    else:
        try:
            for item in context.feature.collected_items:
                shipment = item['shipment_text']
                assert condition == shipment
        except:
            print('No shipment text found')

def extract_number(text):
    match = re.search(r'\d+\.\d+', text)
    if match:
        return float(match.group())
    return None