import boto3
from botocore.exceptions import ClientError
import json

# Working as of 11/13/22. Mostly stolen from someone else

def send_email(item, message):
    SENDER = "email@gmail.com" 
    RECIPIENT = "email@gmail.com" 
    
    AWS_REGION = "us-west-2"


    SUBJECT = f"{item} is in stock"

    BODY_TEXT = (item + " is in stock\r\n")

    BODY_HTML = f"""
    <html>
    <head></head>
    <body>
    <h1> {item} is in stock\r\n</h1>
    <p>{message}</p
  
    </body>
    </html>
                """           


    CHARSET = "UTF-8"


    client = boto3.client('ses',region_name=AWS_REGION)


    try:
    
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
        
                        'Data': BODY_HTML
                    },
                    'Text': {
        
                        'Data': BODY_TEXT
                    },
                },
                'Subject': {

                    'Data': SUBJECT
                },
            },
            Source=SENDER
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def lambda_handler(event, context):
    
    data = event['Records'][0]['body']
    
    data = data.replace("\'", "\"")
    
    
    itemName = (json.loads(data)).get('item')
    print(itemName)
    
    inStock = (json.loads(data)).get('status')
    print(inStock)
    
    testMessage = (json.loads(data)).get('test')
    print(testMessage)
    
    if inStock == "out_of_stock":
        print("not sending email")
        send_email(itemName, testMessage)
    elif inStock == "in_stock":
        print("sending email")
        send_email(itemName, testMessage)
    else:
        print("error")

