import json
from elasticsearch import Elasticsearch

def lambda_handler(event, context):
    ESEndpointUrl = 'https://search-gigglesearch-jsg3pjnauhngf4jnisjjar7hma.us-east-2.es.amazonaws.com'
    es = Elasticsearch(ESEndpointUrl, verify_certs = False)
    httpMethod = event["httpMethod"]
    if httpMethod == 'GET':
        model = event['queryStringParameters']['Model']
        if model == 'user' or model == 'flag' or model == 'vote' or model == 'bubble':
            objectID = event['queryStringParameters']['ObjectID']
            qresult = getObject(objectID,es)
        elif model == 'numVotes':
            objectID = event['queryStringParameters']['ObjectID']
            upvote = event['queryStringParameters']['Upvote']
            qresult = getVotes(objectID, es, upvote)
        elif model == 'getAllBubbles':
            query = event['queryStringParameters']['Query']
            fromNum = event['queryStringParameters']['FromNum']
            sizeNum = event['queryStringParameters']['Size']
            qresult = getBubbles(query, fromNum, sizeNum, es)
    elif httpMethod == 'POST': 
        BubbleID = event['queryStringParameters']['BubbleID']
        CreateDate = event['queryStringParameters']['CreateDate']
        BubbleType = event['queryStringParameters']['BubbleType']
        SeachTerms = event['queryStringParameters']['SeachTerms']
        ImageUrl = event['queryStringParameters']['ImageUrl']
        BubbleContent = event['queryStringParameters']['BubbleContent']
        FlagAction = event['queryStringParameters']['FlagAction']
        UserId = event['queryStringParameters']['UserId']
        UserSocialMedia = event['queryStringParameters']['UserSocialMedia']
        UserProfileImageURL = event['queryStringParameters']['UserProfileImageURL']
        FlagType = event['queryStringParameters']['FlagType']
        Upvote = event['queryStringParameters']['Upvote']
        qresult = es.index(index='bubbles', body= {"BubbleID" : BubbleID,
                                         "CreateDate" : CreateDate,
                                         "BubbleType" : BubbleType,
                                         "SeachTerms" : SeachTerms,
                                         "ImageUrl" : ImageUrl,
                                         "BubbleContent" : BubbleContent,
                                         "FlagAction" : FlagAction,
                                         "UserId" : UserId,
                                         "UserSocialMedia" : UserSocialMedia,
                                         "UserProfileImageURL" : UserProfileImageURL,
                                         "FlagType" : FlagType,
                                         "Upvote" : Upvote})
        if FlagType is not None:
            es.update(index='bubbles',id=BubbleID, body={"doc": {"FlagAction": "flagged"}})
    return {
    'statusCode': "200",
    'body': json.dumps(qresult)
}
    
def getObject(objectID, es):
    return es.search(index ='bubbles', body={'query': {'match': {'_id': objectID}}})

def getVotes(objectID, es, upvote):
    return es.search(index ='bubbles', body={"query":{
    "bool": {
      "must": [
          {"match": {
            "Upvote" : upvote
                    }
    },{
      "match": {
        "BubbleID": objectID
      }}]}
}})

def getBubbles(query,fromNum, sizeNum, es):
    return es.search(index='bubbles', body={"from" : fromNum, "size" : sizeNum, 'query': {'match': {'BubbleContent': query}}})
