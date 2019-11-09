const AWS = require('aws-sdk');
const s3 = new AWS.S3();
const Sharp = require('sharp');
const DynamoDBDocClient = new AWS.DynamoDB.DocumentClient({apiVersion: '2012-08-10'});
const uuidv4 = require('uuid/v4');

const THUMBNAIL_WIDTH = parseInt(process.env.THUMBNAIL_WIDTH, 10);
const THUMBNAIL_HEIGHT = parseInt(process.env.THUMBNAIL_HEIGHT, 10);
const DYNAMODB_PHOTOS_TABLE_NAME = process.env.DYNAMODB_PHOTOS_TABLE_NAME;

exports.handler = async function(event, context) {
  const bucket = event.Records[0].s3.bucket.name; //eslint-disable-line
  const key = event.Records[0].s3.object.key; //eslint-disable-line
  if(key.includes('uploads')) {
    try {
      console.log('Object create in Uploads: ', key);
      const data = await s3.getObject({Bucket: bucket, Key:key}).promise();
      const metadata = data.Metadata;
      console.log(data);
      const originalPhotoDimensions = await Sharp(data.Body).metadata();
      const image = await Sharp(data.Body).resize(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT).toBuffer();
      console.log(image);
      await s3.putObject({
        Bucket: bucket,
        Key: key.replace('uploads', 'thumbnails'),
        Body: image
      }).promise();
      const thumbnail = {
        key: key.replace('uploads', 'thumbnails'),
        width: THUMBNAIL_WIDTH,
        height: THUMBNAIL_HEIGHT
      }
      const fullsize = {
        key: key,
        width: originalPhotoDimensions.width,
			  height: originalPhotoDimensions.height
      }
      const result = await DynamoDBDocClient.put({
        Item: {
          id: uuidv4(),
          owner: metadata.owner,
          photoAlbumId: metadata.albumid,
          bucket: bucket,
          thumbnail: thumbnail,
          fullsize: fullsize,
          createdAt: new Date().getTime()
        },
        TableName: DYNAMODB_PHOTOS_TABLE_NAME
      }).promise();
      console.log(result);
    }
    catch(e) {
      console.log(e);
    }
  }
  context.done(null, 'Successfully processed S3 event'); // SUCCESS with message
};