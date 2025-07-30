#!/usr/bin/env python3
"""
Nova 모델 접근 권한 및 기본 기능 테스트

이 스크립트는 AWS Bedrock의 Nova Micro와 Nova Pro 모델에 대한
접근 권한을 확인하고 기본 기능을 테스트합니다.
"""

import boto3
import json
from botocore.config import Config

def test_bedrock_connection():
    """Bedrock 연결 테스트"""
    try:
        config = Config(
            read_timeout=30,
            connect_timeout=10,
            retries={'max_attempts': 2}
        )
        
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name='us-east-1',
            config=config
        )
        
        print("✅ Bedrock 클라이언트 연결 성공")
        return bedrock_runtime
    except Exception as e:
        print(f"❌ Bedrock 클라이언트 연결 실패: {e}")
        print("💡 AWS 자격 증명을 확인해주세요.")
        return None

def test_nova_micro(client):
    """Nova Micro 모델 테스트"""
    model_id = 'amazon.nova-micro-v1:0'
    
    body = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": "안녕하세요! 간단한 인사말로 응답해주세요."}]
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": 50,
            "temperature": 0.3
        }
    }

    try:
        print("🏃‍♂️ Nova Micro 테스트 중...")
        
        response = client.invoke_model(
            body=json.dumps(body),
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )
        
        response_body = json.loads(response.get('body').read())
        completion = response_body['output']['message']['content'][0]['text']
        
        print(f"✅ Nova Micro 응답: {completion.strip()}")
        return True
        
    except Exception as e:
        print(f"❌ Nova Micro 테스트 실패: {e}")
        if "AccessDeniedException" in str(e):
            print("💡 AWS Console → Bedrock → Model access에서 Nova Micro 접근 권한을 활성화하세요.")
        return False

def test_nova_pro(client):
    """Nova Pro 모델 테스트"""
    model_id = 'amazon.nova-pro-v1:0'
    
    body = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": "Python에 대해 한 문장으로 설명해주세요."}]
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": 100,
            "temperature": 0.5
        }
    }

    try:
        print("🏃‍♀️ Nova Pro 테스트 중...")
        
        response = client.invoke_model(
            body=json.dumps(body),
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )
        
        response_body = json.loads(response.get('body').read())
        completion = response_body['output']['message']['content'][0]['text']
        
        print(f"✅ Nova Pro 응답: {completion.strip()}")
        return True
        
    except Exception as e:
        print(f"❌ Nova Pro 테스트 실패: {e}")
        if "AccessDeniedException" in str(e):
            print("💡 AWS Console → Bedrock → Model access에서 Nova Pro 접근 권한을 활성화하세요.")
        return False

def main():
    print("🧪 Amazon Nova 모델 테스트 시작")
    print("=" * 50)
    
    # Bedrock 연결 테스트
    client = test_bedrock_connection()
    if not client:
        return
    
    print()
    
    # Nova Micro 테스트
    micro_success = test_nova_micro(client)
    print()
    
    # Nova Pro 테스트
    pro_success = test_nova_pro(client)
    print()
    
    # 결과 요약
    print("📊 테스트 결과 요약:")
    print(f"Nova Micro: {'✅ 성공' if micro_success else '❌ 실패'}")
    print(f"Nova Pro: {'✅ 성공' if pro_success else '❌ 실패'}")
    
    if micro_success and pro_success:
        print("\n🎉 모든 테스트 통과! 듀얼 챗봇을 실행할 수 있습니다.")
        print("실행 명령: python nova_dual_chatbot.py")
    else:
        print("\n⚠️  일부 모델에 접근할 수 없습니다.")
        print("AWS Console → Bedrock → Model access에서 모델 접근 권한을 확인하세요.")
        print("참고: https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html")

if __name__ == "__main__":
    main()
