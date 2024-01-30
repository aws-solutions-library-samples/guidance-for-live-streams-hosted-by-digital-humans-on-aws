import os
import sys
import json
import boto3
import botocore
from typing import List

import time
from contextlib import closing
import tempfile
import urllib3
from botocore.exceptions import ClientError
import decimal
from boto3.dynamodb.conditions import Key, Attr




# global variables

DDB_TABLE = 'vr-demo'
S3_BUCKET = os.getenv('S3_BUCKET')
S3_PREFIX = 'material/mp3/'
WEB_PREFIX= os.getenv('CLOUDFRONT_PREFIX')
contentType = "application/json"
accept = "*/*"

cors = {
    "Access-Control-Allow-Headers" : "Content-Type",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)
        
languageCode = 'cmn-CN'
voiceId = 'Zhiyu'
speed_prefix = '<prosody rate="medium">'
camera='side_stand'
question=''
template='我是数字助手，请问如何帮助您'


def lambda_handler(event, context):

    # print(event, type(event))
    data = json.loads(event.get('body'))
    # print(data, type(data))
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
    role=data.get('role')
    print('选择角色')
    
    if role=='role_tourist_guide':
        languageCode='cmn-CN'
        voiceId='Zhiyu'
        character='rp_emma_female_white'
        template='你是一名导游，名叫小林，请用风趣的方式，30字以内，回答如下问题:'
        
        
    elif role=='role_expert_AWS':
        languageCode='cmn-CN'
        voiceId='Zhiyu'
        character='rp_rin_female_asian'
        template='你是一名亚马逊云科技专家，名叫艾玛，请用专业的方式，30字以内，回答如下问题:'
        
  
    elif role=='role_expert_auto_en':
        languageCode='en-GB'
        voiceId='Brian'  
        character='rp_brandon_male_white'
        template='你是一名汽车领域的专家，名字叫做Kai，请用专业的方式，20字以内，使用英语回答下面问题:'
        
    
    elif role=='role_3D_avatar_en':
        languageCode='en-GB'
        voiceId='Brian'  
        character='rp_ming_male_asian'
        template='你是Ming Qi的数字分身，请用活泼的方式，30字以内，使用英语回答如下问题:'
       
    
    elif role=='role_expert_auto_cn':
        languageCode='cmn-CN'
        voiceId='Zhiyu'
        character='rp_deloris_female_asian'
        template='你是一名医疗健康的专家，名叫小美，请用专业的方式，30字以内，回答如下问题:'
        
    

    print('等待智能搜索，大语言模型回复。。。。')
    bedrock = boto3.client(service_name='bedrock-runtime')
    
    question=template+text
    print(question)

    text=bedrock_chat(bedrock,question)
    
    print('智能搜索，大语言模型回复:', text)
        
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
  
    image_file = image_url.split('/')[-1]

    base_filename = str(int(time.time()))
    
    dest_mp3_s3_url = S3_PREFIX + base_filename + '.mp3'

    # print(dest_mp3_s3_url)
    # print(WEB_PREFIX + dest_mp3_s3_url)
    print('文字转语音。。。')
    

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
   
            print('文字转语音完成')

                    
            print('blendshape完成')
                    
            client = boto3.client('dynamodb')
            
            #write to DDB
            image_url='https://d2a5lerx865rzn.cloudfront.net/Slide6.jpeg'
            
            client = boto3.client('dynamodb')
            response = client.put_item(
                TableName=DDB_TABLE,
                Item={
                    'demo_name': {'S': "VR-demo"},
                    'index': {'S': "0001"},
                    'pic_path': {'S': image_url},
                    'audio_path': {'S': WEB_PREFIX + dest_mp3_s3_url},
                    'text': {'S': text},
                    'character': {'S': character},
                    'voice': {'S': voice},
                    'scene': {'S': scene},
                    'action': {'S': action},
                    'item_id': {'S': item_id},
                    'user_id': {'S': user_id},
                    'random_id': {'S': index},
                    'playing': {'BOOL': True},
                    'voice_speed': {'S': voice_speed},
                    'vr_module': {'S': vr_module},
                    'camera':{'S':camera}
                }
                )
            print('数字人驱动。。。')
    return {
        'statusCode': 200,
        'headers': cors,
        'body': "success"
    }

    

def generate_prompt(text):
    prompts = ""
    prompts += "Human:"
    prompts+="\n"
    prompts+=text
    prompts+="\nAssistant:"
    return prompts

def bedrock_chat(bedrock,question):
    response_from_bedrock= bedrock.invoke_model(body=json.dumps(
        {"prompt":generate_prompt(question),
        "max_tokens_to_sample":300,
        "temperature":0.1,
        "top_k":10,
        "top_p":0.1,
        "stop_sequences":[]
        }),
        modelId="anthropic.claude-v2",
        accept=accept,
        contentType=contentType)
    response_body = json.loads(response_from_bedrock.get('body').read())
    print(response_body)
    answer = response_body.get('completion')
    return answer