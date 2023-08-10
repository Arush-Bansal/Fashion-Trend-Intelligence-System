from selenium import webdriver
import time
import json
from imageDownload import saveImage

TIME_DELAY = 0
PAGE_COUNT = 4
# PAGE_COUNT = 1

def dressUrl(page : int) : 
    return f"https://www.myntra.com/dresses?f=Gender%3Amen%20women%2Cwomen&p={page}"

def topsUrl(page : int) : 
    return f"https://www.myntra.com/tops?p={page}"

def clickMore(driver : webdriver.Chrome):
    driver.find_element_by_class_name('index-showMoreText').click()

def getProductLinks(url : str, driver : webdriver.Chrome):
    driver.get(url)
    time.sleep(TIME_DELAY)
    urlLinks = driver.execute_script("return [...document.querySelectorAll('.product-base')].map(ele => ele.querySelector('a').href)")
    return urlLinks

def specToObj(specList : [str]):
    returnObj = {}
    for spec in specList:
        [key, value] = spec.split("\n")
        returnObj[key] = value
    return returnObj

def productDetails(url : str, driver : webdriver.Chrome):
    driver.get(url)
    time.sleep(TIME_DELAY)

    price = driver.execute_script("return document.querySelector('strong').innerText")
    productTitle = driver.execute_script("return document.querySelector('.pdp-title').innerText")
    productDesc = driver.execute_script("return document.querySelector('.pdp-name').innerText")
    productDetails = driver.execute_script("return document.querySelector('.pdp-product-description-content').innerText")

    driver.execute_script("document.querySelector('.index-showMoreText').click()")
    specs = specToObj(driver.execute_script("return [...document.querySelectorAll('.index-row')].map(ele => ele.innerText)"))
     
    imageURL = driver.execute_script("return document.querySelector('.image-grid-image').style.backgroundImage").strip().split('"')[1]
    rating = driver.execute_script("return (document.querySelector('.index-averageRating') !== null) ? document.querySelector('.index-averageRating').innerText : -1")
    varifiedUsers = driver.execute_script("return (document.querySelector('.index-countDesc') !==null) ? document.querySelector('.index-countDesc').innerText : 0")
    if type(varifiedUsers) == str : varifiedUsers = varifiedUsers.split()[0]

    saveImage(imageURL, productTitle)

    return {
        "imageURL" : imageURL,
        "price" : price,
        "productTitle" : productTitle,
        "productDesc" : productDesc,
        "productDetails" :productDetails,
        "specs" : specs,
        "rating" : rating,
        "varifiedUsers" : varifiedUsers,
    }


driver = webdriver.Chrome("chromedriver")
productURLs = []
for i in range(1, PAGE_COUNT + 1):
    productURLs.extend(getProductLinks(dressUrl(i), driver))
for i in range(1, PAGE_COUNT + 1):
    productURLs.extend(getProductLinks(topsUrl(i), driver))

with open("data.json", "w") as json_file:
    data = []
    # data.append(productDetails(productURLs[0], driver))
    # data.append(productDetails(productURLs[1], driver))
    # data.append(productDetails(productURLs[2], driver))
    # data.append(productDetails(productURLs[3], driver))
    for url in productURLs:
        data.append(productDetails(url, driver))
    json.dump(data, json_file)

driver.quit()
