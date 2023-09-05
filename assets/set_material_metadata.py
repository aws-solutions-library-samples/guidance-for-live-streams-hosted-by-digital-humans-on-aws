import os
import time
import json
import boto3
from contextlib import closing
import tempfile
import urllib3

# global variables

DDB_TABLE = 'vr-demo'
S3_BUCKET = os.getenv('S3_BUCKET')
S3_PREFIX = 'material/mp3/'
WEB_PREFIX= os.getenv('CLOUDFRONT_PREFIX')
cors = {
    "Access-Control-Allow-Headers" : "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

languageCode = 'cmn-CN'
voiceId = 'Zhiyu'
speed_prefix = '<prosody rate="medium">'
camera='side_stand'

def lambda_handler(event, context):
    


    print(event, type(event))
    data = json.loads(event.get('body'))
    print(data, type(data))
    user_id=data.get('user_id','')
    index = data.get('id', '')
    text = data.get('text', '')
    image_url = data.get('image_url', '')
    character=data.get('character','')
    voice=data.get('voice','')
    scene=data.get('scene','')
    action=data.get('action','')
    item_id=data.get('item_id','')
    voice_speed=data.get('voice_speed','')
    vr_module=data.get('vr_module','')
    camera=data.get('camera','')
    
    print(user_id)
    print(index)
    
    
    
    print(text)
    
    if len(text) == 0:
        text="."
        
    if voice_speed=='medium' or voice_speed=='':
        speed_prefix='<prosody rate="medium">'
    elif voice_speed=='slow':
        speed_prefix='<prosody rate="slow">'
    elif voice_speed=='x-slow':
        speed_prefix='<prosody rate="x-slow">'
    elif voice_speed=='fast':
        speed_prefix='<prosody rate="fast">'
    elif voice_speed=='x-fast':
        speed_prefix='<prosody rate="x-fast">'
    else:
        speed_prefix='<prosody rate="medium">'

    ssmltext='<speak>'+speed_prefix+text+'</prosody></speak>'
    
    if voice=='Zhiyu-CHN':
        languageCode='cmn-CN'
        voiceId='Zhiyu'
    elif voice=='US-En-Male':
        languageCode='en-US'
        voiceId='Joey'
    elif voice=='US-En-Female':
        languageCode='en-US'
        voiceId='Salli'
    elif voice=='UK-En-Male':
        languageCode='en-GB'
        voiceId='Brian'    
    elif voice=='UK-En-Female':
        languageCode='en-GB'
        voiceId='Emma'
    elif voice=='fr-FR-Female':
        languageCode='fr-FR'
        voiceId='Lea'
    elif voice=='DE-Female':
        languageCode='de-DE'
        voiceId='Vicki'  
    elif voice=='DE-Male':
        languageCode='de-DE'
        voiceId='Daniel'  
        
    #generate mp3 file name, reuse image name
    
    image_file = image_url.split('/')[-1]
    base_filename = image_file.split('.')[0]
    
    dest_mp3_s3_url = S3_PREFIX + base_filename + '.mp3'

    print(dest_mp3_s3_url)
    print(WEB_PREFIX + dest_mp3_s3_url)
    

    c = boto3.client('polly',region_name='us-east-1')
    

    
    rs = c.synthesize_speech(
        # Engine='standard',
        Engine='neural',
        LanguageCode=languageCode,
        OutputFormat='mp3',
        Text=ssmltext,
        # TextType='text',
        TextType='ssml',
        VoiceId=voiceId
    )
    
    s3 = boto3.client('s3')
    with tempfile.NamedTemporaryFile('ab') as ntf:
        with closing(rs['AudioStream']) as stream:
            #body = stream.read()
            ntf.write(stream.read())
            #ntf.seek(0)
            s3.upload_file(ntf.name, S3_BUCKET, dest_mp3_s3_url, ExtraArgs={'ContentType': "audio/mpeg"})
            
            
    
       
            w2j_url = 'https://open.caldron.cn/wav2json-a7adc817c6'
            w2j_param = {
                "hostapi_api_key": "nj8JSFPTgm2V7zl",
                "bs_type": "52",
                "input_url": WEB_PREFIX + dest_mp3_s3_url
            }
            http = urllib3.PoolManager()
            res = http.request('POST', w2j_url, body=json.dumps(w2j_param),headers={'Content-Type': 'application/json'})
            
            res_data = res.data.decode()
            res_data = json.loads(res_data)
            bs_url = ''
            if res_data.get('taskid'):
                cnt = 0
                w2j_url_get = f"https://open.caldron.cn/wav2json-a7adc817c6?hostapi_api_key=nj8JSFPTgm2V7zl&taskid={res_data['taskid']}"
                while cnt < 60:
                    res = http.request('GET', w2j_url_get)
                    res_data_res = res.data.decode()
                    res_data_res = json.loads(res_data_res)
                    print(type(res_data_res), res_data_res)
                    if res_data_res.get('data') and res_data_res['data'].get('callback_data'):
                        bs_url = res_data_res['data']['callback_data']['output_url']
                        break
                    elif res_data_res['code'] == 400:
                        break
                    cnt += 1
                    time.sleep(2)
                    
            client = boto3.client('dynamodb')
            #write to DDB
            

        
            client = boto3.client('dynamodb')
            response = client.put_item(
                TableName=DDB_TABLE,
                Item={
                    'demo_name': {'S': user_id},
                    'index': {'S': index},
                    'pic_path': {'S': image_url},
                    'bs_url': {'S': bs_url},
                    'audio_path': {'S': WEB_PREFIX + dest_mp3_s3_url},
                    'text': {'S': text},
                    'character': {'S': character},
                    'voice': {'S': voice},
                    'scene': {'S': scene},
                    'action': {'S': action},
                    'item_id': {'S': item_id},
                    'user_id': {'S': user_id},
                    'random_id': {'S': ''},
                    'playing': {'BOOL': False},
                    'voice_speed': {'S': voice_speed},
                    'vr_module': {'S': vr_module},
                    'camera':{'S':camera}
                })
    return {
        'statusCode': 200,
        'headers': cors,
        'body': "success"
    }