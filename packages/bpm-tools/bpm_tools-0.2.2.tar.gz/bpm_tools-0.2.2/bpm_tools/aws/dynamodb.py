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
        dynamodbTableRes ( [boto3.resource('dynamodb').Table], optional): [description]. Defaults to None.

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



def get_records_by_key_condition(tablename,KeyConditionExpression,session = boto3.Session(), dynamodbTableRes = None):
    """Given a KeyConditionExpression and DynamoDB table (either name or resource object)
        function queries the DDB table and returns the result

    Args:
        tablename ([type]): [description]
        KeyConditionExpression ([type]): [description]
        session ([type], optional): [description]. Defaults to boto3.Session().
        dynamodbTableRes ([type], optional): [description]. Defaults to None.

    Returns:
        dict: Results of the query
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

    result = dynamodbTableRes.query(KeyConditionExpression=KeyConditionExpression)
    return result



def delete_items_by_hashkey(dynamodbTableRes,hashkey):
    """Given a dynamoDB table resource and a hashkey this function 
    deletes all corresponding records

    For tables with a hash and range key, this function can delete
    several records at once.

    Args:
        dynamodbTableRes ([type]): Boto3 DDB table resource
        hashkey (bool): Hashkey of records to delete

    Returns:
        [type]: [description]
    """
    
    
    
    hashKeyName = None
    rangeKeyName = None

    # Get the HASH and RANGE key names
    for ddbkey in table.key_schema:
        KeyType = ddbkey['KeyType']
        AttributeName  = ddbkey['AttributeName']

        if KeyType == 'HASH':
            hashKeyName = AttributeName

        elif KeyType == 'RANGE':
            rangeKeyName = AttributeName

    # If table has a HASH key
    if hashKeyName is not None:
        KeyConditionExpression = Key(hashKeyName).eq(hashkey)
        # Get all the items corresponding to the hashkey
        result = get_records_by_key_condition(tablename = "",KeyConditionExpression= KeyConditionExpression,dynamodbTableRes = table)



        # Delete items in batch - Include rangeKey if required
        with table.batch_writer() as batch:
            print("Deleting ", len(result['Items']), " items....")
            for row in result['Items']:
                if rangeKeyName is not None:
                    batch.delete_item(
                        Key={
                            hashKeyName: hashkey,
                            rangeKeyName: row[rangeKeyName]
                        }
                    )
                else:
                    batch.delete_item(
                        Key={
                            hashKeyName: hashkey
                        }
                    )
                
    else:
        return "Invalid table..."
