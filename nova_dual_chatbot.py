#!/usr/bin/env python3
"""
Amazon Bedrock Nova 듀얼 모델 챗봇
Nova Micro: 즉각적인 초기 응답
Nova Pro: 상세한 최종 답변

GitHub: https://github.com/your-username/amazon-nova-dual-chatbot
"""

import boto3
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from botocore.config import Config

class NovaDualChatbot:
    def __init__(self, region='us-east-1'):
        """
        Bedrock 클라이언트 초기화
        
        Args:
            region (str): AWS 리전 (기본값: us-east-1)
        """
        # 타임아웃 설정으로 안정성 향상
        config = Config(
            read_timeout=60,
            connect_timeout=10,
            retries={'max_attempts': 3}
        )
        
        try:
            self.bedrock_runtime = boto3.client(
                service_name='bedrock-runtime',
                region_name=region,
                config=config
            )
            print(f"✅ Bedrock 클라이언트 초기화 완료 (리전: {region})")
        except Exception as e:
            print(f"❌ Bedrock 클라이언트 초기화 실패: {e}")
            print("💡 AWS 자격 증명과 리전 설정을 확인해주세요.")
            sys.exit(1)
    
    def invoke_nova_micro(self, prompt: str) -> str:
        """
        Nova Micro 모델 호출 - 즉각적인 초기 응답
        
        Args:
            prompt (str): 입력 프롬프트
            
        Returns:
            str: Nova Micro의 응답
        """
        model_id = 'amazon.nova-micro-v1:0'
        
        # Nova Micro용 요청 본문
        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [{"text": prompt}]
                }
            ],
            "inferenceConfig": {
                "max_new_tokens": 100,
                "temperature": 0.3
            }
        }

        try:
            print("🏃‍♂️ Nova Micro 호출 중...")
            start_time = time.time()
            
            response = self.bedrock_runtime.invoke_model(
                body=json.dumps(body),
                modelId=model_id,
                accept='application/json',
                contentType='application/json'
            )
            
            # 응답 파싱
            response_body = json.loads(response.get('body').read())
            completion = response_body['output']['message']['content'][0]['text']
            
            end_time = time.time()
            print(f"⚡ Nova Micro 응답 완료 ({end_time - start_time:.2f}초)")
            
            return completion.strip()
            
        except Exception as e:
            print(f"❌ Nova Micro 호출 오류: {e}")
            return "죄송합니다. 초기 응답 생성에 문제가 발생했습니다."

    def stream_nova_pro(self, prompt: str):
        """
        Nova Pro 모델 스트리밍 호출 - 상세한 최종 답변
        
        Args:
            prompt (str): 입력 프롬프트
            
        Yields:
            str: Nova Pro의 스트리밍 응답 청크
        """
        model_id = 'amazon.nova-pro-v1:0'
        
        # Nova Pro용 요청 본문
        body = {
            "messages": [
                {
                    "role": "user", 
                    "content": [{"text": prompt}]
                }
            ],
            "inferenceConfig": {
                "max_new_tokens": 2048,
                "temperature": 0.5
            }
        }

        try:
            print("🏃‍♀️ Nova Pro 스트리밍 시작...")
            
            response = self.bedrock_runtime.invoke_model_with_response_stream(
                body=json.dumps(body),
                modelId=model_id,
                accept='application/json',
                contentType='application/json'
            )
            
            # 스트리밍 응답 처리
            stream = response.get('body')
            if stream:
                for event in stream:
                    chunk = event.get('chunk')
                    if chunk:
                        chunk_obj = json.loads(chunk.get('bytes').decode())
                        
                        # contentBlockDelta에서 텍스트 추출
                        if 'contentBlockDelta' in chunk_obj:
                            delta = chunk_obj['contentBlockDelta'].get('delta', {})
                            text_content = delta.get('text', '')
                            if text_content:
                                yield text_content

        except Exception as e:
            print(f"❌ Nova Pro 스트리밍 오류: {e}")
            yield "\n죄송합니다. 상세 답변 생성 중 오류가 발생했습니다."

    def create_prompts(self, user_query: str):
        """
        각 모델에 맞는 프롬프트 생성
        
        Args:
            user_query (str): 사용자 질문
            
        Returns:
            tuple: (micro_prompt, pro_prompt)
        """
        micro_prompt = f"""사용자가 다음 질문을 했습니다: "{user_query}"

당신은 친절한 AI 어시스턴트입니다. 질문을 이해했으며, 상세한 답변을 준비하고 있다는 내용의 짧고 격려하는 한 문장으로 응답해주세요. 한국어로 답변하세요."""

        pro_prompt = f"""다음 질문에 대해 전문가 수준의 상세하고 구조화된 답변을 제공해주세요. 
복잡한 주제는 이해하기 쉽게 나누어 설명하고, 필요한 경우 마크다운을 사용하여 서식을 지정해주세요.
한국어로 답변하세요.

질문: "{user_query}" """

        return micro_prompt, pro_prompt

    def chat(self, user_query: str):
        """
        듀얼 모델 오케스트레이션 메인 함수
        
        Args:
            user_query (str): 사용자 질문
        """
        print(f"\n💬 사용자 질문: {user_query}")
        print("=" * 60)
        
        # 각 모델용 프롬프트 생성
        micro_prompt, pro_prompt = self.create_prompts(user_query)
        
        # ThreadPoolExecutor로 병렬 실행
        with ThreadPoolExecutor(max_workers=2) as executor:
            # 두 작업을 동시에 시작
            future_micro = executor.submit(self.invoke_nova_micro, micro_prompt)
            future_pro_stream = executor.submit(self.stream_nova_pro, pro_prompt)

            # Nova Micro 응답 먼저 출력
            micro_response = future_micro.result()
            print(f"\n🚀 [초기 응답 - Nova Micro]")
            print(f"💭 {micro_response}")
            
            # Nova Pro 스트리밍 응답 출력
            print(f"\n📚 [상세 답변 - Nova Pro]")
            pro_stream_generator = future_pro_stream.result()
            
            full_pro_response = ""
            for chunk in pro_stream_generator:
                # 실시간 타이핑 효과
                sys.stdout.write(chunk)
                sys.stdout.flush()
                full_pro_response += chunk
                
            print(f"\n\n✅ 응답 완료!")
            print("=" * 60)

def main():
    """
    메인 실행 함수
    """
    print("🤖 Amazon Nova 듀얼 모델 챗봇")
    print("Nova Micro + Nova Pro 조합으로 빠르고 정확한 답변을 제공합니다.")
    print("=" * 60)
    
    # 챗봇 인스턴스 생성
    try:
        chatbot = NovaDualChatbot()
    except Exception as e:
        print(f"❌ 챗봇 초기화 실패: {e}")
        return
    
    # 테스트 질문들
    test_queries = [
        "AWS Lambda와 EC2의 차이점을 설명해주세요.",
        "머신러닝에서 오버피팅이란 무엇인가요?",
        "Python의 리스트와 튜플의 차이점은?",
        "클라우드 컴퓨팅의 장점을 알려주세요."
    ]
    
    # 대화형 모드 또는 테스트 모드 선택
    print("모드를 선택하세요:")
    print("1: 대화형 모드 (직접 질문 입력)")
    print("2: 테스트 모드 (미리 준비된 질문)")
    
    mode = input("선택 (1 또는 2): ").strip()
    
    if mode == "1":
        # 대화형 모드
        print("\n💡 질문을 입력하세요 (종료하려면 'quit' 입력):")
        while True:
            user_input = input("\n🙋‍♂️ 질문: ").strip()
            if user_input.lower() in ['quit', 'exit', '종료']:
                print("👋 챗봇을 종료합니다.")
                break
            if user_input:
                chatbot.chat(user_input)
    
    elif mode == "2":
        # 테스트 모드
        print(f"\n🧪 테스트 모드: {len(test_queries)}개 질문으로 테스트합니다.")
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 테스트 {i}/{len(test_queries)}")
            chatbot.chat(query)
            
            if i < len(test_queries):
                input("\n⏸️  다음 테스트로 진행하려면 Enter를 누르세요...")
    
    else:
        print("❌ 잘못된 선택입니다. 1 또는 2를 입력해주세요.")

if __name__ == "__main__":
    main()
