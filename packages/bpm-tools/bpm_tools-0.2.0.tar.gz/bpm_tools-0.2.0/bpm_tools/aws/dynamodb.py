import json
import boto3
import os
from datetime import datetime

#Required to to convert the incoming json event to decimal (DynamoDB does not accept floating point!)
from decimal import Decimal


#Removes invalid values that can't be inserted into DynamoDB
def clean_empty(d):
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (clean_empty(v) for v in d) if v is not None and str(v) != '']
    return {k: v for k, v in ((k, clean_empty(v)) for k, v in d.items()) if v is not None and str(v) != ''}


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)



""" 
---------------------------- update_dynamodb_item -----------------------------
*
*
* Updates a record with values specified in updateMsg dictionary:
*
*
* Input:
*   tablename: dynamodb table name
*   itemKey:  The key of the item to be updated
*   updateMsg: A dictionary of values to set for the dynamodb item
*
* Note:
*   If the item does not exist a new item will be created
*   First level keys in dictionary will be updated/added
*   Updates of values inbedded in a map (e.g. second level of updateMsg) is not supported.
*   Second level dictionaries will overwrite all data in existing maps 
*
----------------------------------------------------------------------------------------------
"""



def update_dynamodb_item(tablename, itemKey = {}, updateMsg = {},session = boto3.Session(), dynamodbTableRes = None):
    """[summary]

    Args:
        tablename ([type]): [description]
        itemKey (dict, optional): [description]. Defaults to {}.
        updateMsg (dict, optional): [description]. Defaults to {}.
        session ([boto3.Session()], optional): [description]. Defaults to boto3.Session().
        table_res ( [boto3.resource('dynamodb').Table], optional): [description]. Defaults to None.

    Returns:
        [type]: [description]
    """

    
   
    try:
        # Create new DynamoDB resource and table (Locally accessible)
        if dynamodbTableRes is None:
            dynamodb = session.resource('dynamodb')
            dynamodbTableRes = dynamodb.Table(tablename)
        
         # Otherwise use the table resource passed to the function
        else:
            pass

    except Exception as e:
        print("Error opening the DynamoDb tables", e)
        return False

    #Add update timestamp and clean update data
    now = datetime.now()
    updated_at = now.strftime ("%Y-%m-%d %H:%M:%S")
    updateMsg['last_update_at'] = updated_at
    updateMsgCleaned = clean_empty(updateMsg)

    #----------------------------------------------------------------------------------------
    #STEP 2 -  Update the request status in the DATA_REQUESTS_DYNAMODB_TABLE
    #----------------------------------------------------------------------------------------    
    try:
        #Building the update query
        UpdateExpression = 'set '
        ExpressionAttributeValues = {}
        ExpressionAttributeNames={}
        i = 0
        for key, value in updateMsgCleaned.items():            

            fieldRef = ':' +  str(i) 
            UpdateExpression += '#' + str(key) + '=' + fieldRef + ','
            ExpressionAttributeValues[fieldRef] = value
            ExpressionAttributeNames['#' + str(key)] = str(key)
            
            i+=1

        #Update the table
        response = dynamodbTableRes.update_item(
            Key=itemKey,
            UpdateExpression=UpdateExpression[:-1],
            ExpressionAttributeValues=ExpressionAttributeValues,
            ExpressionAttributeNames = ExpressionAttributeNames,
            ReturnValues="UPDATED_NEW"
        )


    except Exception as e:
        print(e)
        return False

    else:

        return True
