const AWS = require('aws-sdk')
AWS.config.update({ region: process.env.AWS_REGION })
const s3 = new AWS.S3()
// Change this value to adjust the signed URL's expiration
const URL_EXPIRATION_SECONDS = 300
// Main Lambda entry point

const cors = {
    "Access-Control-Allow-Headers" : "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

exports.handler = async (event) => {
      // TODO implement
    const randomID = parseInt(Math.random() * 10000000)
    const Key = `material/image/${randomID}.jpg`

    // // Get signed URL from S3
    const s3Params = {
    Bucket: process.env.S3_BUCKET,
    Key,
    Expires: URL_EXPIRATION_SECONDS,
    ContentType: 'image/jpeg',

    // This ACL makes the uploaded object publicly readable. You must also uncomment
    // the extra permission for the Lambda function in the SAM template.

    // ACL: 'public-read'
    }

    console.log('Params: ', s3Params)
    const uploadURL = await s3.getSignedUrlPromise('putObject', s3Params)

    // return JSON.stringify({
    // uploadURL: uploadURL,
    // Key
    // }) 
     
      
    const response = {
        statusCode: 200,
        headers:cors,
        body: JSON.stringify({
    uploadURL: uploadURL,Key
    })
    };
    return response;

//   //return await getUploadURL()
}


