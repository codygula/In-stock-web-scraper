import json
from bs4 import BeautifulSoup
from urllib.request import urlopen
import boto3

##### EDIT HERE AS NEEDED #####

item = "ZimaBoard 216 $120 x86 SBC"
site = "https://shop.zimaboard.com/products/zimaboard-single-board-server-for-creators-8g-32gb-linux-windows-openwrt-pfsense-andorid-libreelec-development-board-low-cost-hackable-single-board-server?variant=39283928400070"
textString = "Sold out"

###############################


client = boto3.client('sqs')

def lambda_handler(event, context):
    
    try:
        html = urlopen(site).read().decode('utf-8')
    
        soup = BeautifulSoup(html, "html.parser")
    
        ##### EDIT HERE AS NEEDED #####
        
        results = soup.find(id="ProductSelect-product-template")
    
        element = results.find("option", value="39283928400070")
        
        ###############################
        
        print(element.text)
        
        if textString in element.text:
            print("Testing OUT OF STOCK")
            response = client.send_message(
                QueueUrl='https://sqs.us-west-2.amazonaws.com/929749464795/scraperqueue',
                MessageBody=str({
                    "item": item,
                    "status": "out_of_stock",
                    "test": "Test message"
                }))
            print(response)
        
        else:
            print("Testing NOT OUT OF STOCK")
            response = client.send_message(
                QueueUrl='https://sqs.us-west-2.amazonaws.com/929749464795/scraperqueue',
                MessageBody=str({
                    "item": item,
                    "status": "in_stock",
                    "test": "element name change"
                }))
            print(response)    
        
        try:
            print("element.text = " , element.text)
        except:
            print("element.text PRINT ERROR")
                

        
        
    except:
        print("not out of stock SCRAPER ERROR")
        response = client.send_message(
            QueueUrl='https://sqs.us-west-2.amazonaws.com/929749464795/scraperqueue',
            MessageBody=str({
                "item": item,
                "status": "in_stock",
                "test": "scraper_error"
            }))
        print(response)
    
        
    
    
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
