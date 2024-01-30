const AWS = require('aws-sdk');
const dynamoDb = new AWS.DynamoDB.DocumentClient();
const params = {
    TableName: 'vr-demo'
};
const cors = {
    "Access-Control-Allow-Headers" : "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}
module.exports.handler = async (event) => {
    console.log("data",event);
    
    var bodyJson=JSON.parse(event['body']);
    //var bodyJson=event['body'];
    var id = bodyJson.id;
    var random_id = bodyJson.random_id;
    var vr_module=bodyJson.vr_module; 
    //console.log(id);
    //console.log(random_id);
    
    const items = await dynamoDb.scan({
        TableName: params.TableName,
    }).promise();
    let request = [];
    for (let item of items.Items) {
        if(vr_module==item.vr_module){
            item.playing = item.index == id; // todo: be careful the name
            if(item.playing==true){
            item.random_id=random_id;
            }
   
        }
        
        request.push({
            PutRequest: {
                Item: item
            }
        });
    }
    let requestItems = {};
    requestItems[params.TableName] = request;
    const batchWriteReq = {
        RequestItems: requestItems
    };
    await dynamoDb.batchWrite(batchWriteReq).promise();
    
    
    const response = {
        statusCode: 200,
        headers: cors,
        body: JSON.stringify(items.Items)
    };
    return response;
};
  