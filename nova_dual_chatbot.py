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
    
    def stream_nova_micro(self, prompt: str):
        """
        Nova Micro 모델 스트리밍 호출 - 즉각적인 초기 응답
        
        Args:
            prompt (str): 입력 프롬프트
            
        Yields:
            str: Nova Micro의 스트리밍 응답 청크
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
                "max_new_tokens": 500,  # 400에서 500으로 증가
                "temperature": 0.3
            }
        }

        try:
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
            yield f"❌ Nova Micro 스트리밍 오류: {e}"

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
            yield f"❌ Nova Pro 스트리밍 오류: {e}"

    def create_prompts(self, user_query: str):
        """
        각 모델에 맞는 프롬프트 생성
        
        Args:
            user_query (str): 사용자 질문
            
        Returns:
            tuple: (micro_prompt, pro_prompt)
        """
        micro_prompt = f"""다음 질문에 대해 간결하고 완결된 개요를 제공해주세요: "{user_query}"

요구사항:
- 핵심 내용을 1-2개 문단으로 간단명료하게 설명 (너무 길지 않게)
- 반드시 완전한 문장으로 마무리할 것
- 마지막에 "더 구체적으로 살펴보겠습니다." 같은 간단한 연결 문구로 마무리
- 한국어로 답변하세요

중요: 간결하게 작성하여 답변이 중간에 끊어지지 않도록 해주세요."""

        pro_prompt = f"""앞서 "{user_query}"에 대한 기본적인 개요를 제공했습니다. 
이제 그 내용에 자연스럽게 이어서 더 상세하고 전문적인 분석을 제공해주세요.

요구사항:
- 앞선 답변의 자연스러운 연장선상에서 시작 (예: "더 구체적으로 살펴보면...", "이를 더 자세히 분석하면..." 등)
- 구체적인 예시, 장단점, 사용 사례, 비교 분석을 포함한 심화 내용
- 마크다운을 활용한 체계적이고 구조화된 답변
- 실무적이고 전문적인 관점에서의 깊이 있는 설명
- 한국어로 답변하세요

답변 스타일: 전문적이면서도 이해하기 쉽게, 논리적으로 구성하여 완전한 가이드가 되도록"""

        return micro_prompt, pro_prompt

    def chat(self, user_query: str):
        """
        듀얼 모델 오케스트레이션 메인 함수
        
        Args:
            user_query (str): 사용자 질문
        """
        print(f"\n💬 질문: {user_query}")
        print("=" * 60)
        
        # 각 모델용 프롬프트 생성
        micro_prompt, pro_prompt = self.create_prompts(user_query)
        
        print("🤖 답변:")
        
        # Pro 모델의 스트리밍 결과를 저장할 버퍼
        pro_buffer = []
        pro_complete = False
        
        def collect_pro_stream():
            """Pro 모델의 스트리밍 결과를 버퍼에 수집"""
            nonlocal pro_buffer, pro_complete
            try:
                for chunk in self.stream_nova_pro(pro_prompt):
                    pro_buffer.append(chunk)
                pro_complete = True
            except Exception as e:
                pro_buffer.append(f"\n❌ Nova Pro 오류: {e}")
                pro_complete = True
        
        # ThreadPoolExecutor로 병렬 실행
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Pro 모델을 백그라운드에서 시작
            future_pro = executor.submit(collect_pro_stream)
            
            # 1단계: Nova Micro 스트리밍 (빠른 초기 응답)
            print("🏃‍♂️ Nova Micro 스트리밍 시작...")
            try:
                for chunk in self.stream_nova_micro(micro_prompt):
                    sys.stdout.write(chunk)
                    sys.stdout.flush()
                    time.sleep(0.02)  # 자연스러운 타이핑 효과
                
                # Micro 완료 후 줄바꿈
                print("\n")
                
            except Exception as e:
                print(f"❌ Nova Micro 오류: {e}")
                print("\n")
            
            # 2단계: Pro 모델 결과 출력 (버퍼에서 가져와서 스트리밍처럼 출력)
            buffer_index = 0
            
            while not pro_complete or buffer_index < len(pro_buffer):
                # 버퍼에 새로운 내용이 있으면 출력
                while buffer_index < len(pro_buffer):
                    chunk = pro_buffer[buffer_index]
                    sys.stdout.write(chunk)
                    sys.stdout.flush()
                    time.sleep(0.01)  # 약간 더 빠른 타이핑 효과
                    buffer_index += 1
                
                # Pro 모델이 아직 완료되지 않았다면 잠시 대기
                if not pro_complete:
                    time.sleep(0.05)
            
            # Pro 작업 완료 대기
            future_pro.result()
        
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
