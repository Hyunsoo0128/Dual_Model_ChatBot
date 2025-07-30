#!/usr/bin/env python3
"""
Amazon Nova 듀얼 모델 챗봇 사용 예제

이 예제는 다양한 시나리오에서 챗봇을 사용하는 방법을 보여줍니다.
"""

import sys
import os

# 상위 디렉토리의 모듈을 import하기 위해 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nova_dual_chatbot import NovaDualChatbot

def example_technical_questions():
    """기술적 질문 예제"""
    print("🔧 기술적 질문 예제")
    print("=" * 40)
    
    chatbot = NovaDualChatbot()
    
    technical_questions = [
        "Docker와 Kubernetes의 차이점을 설명해주세요.",
        "RESTful API의 설계 원칙은 무엇인가요?",
        "데이터베이스 정규화란 무엇인가요?"
    ]
    
    for i, question in enumerate(technical_questions, 1):
        print(f"\n📝 예제 {i}: {question}")
        chatbot.chat(question)
        
        if i < len(technical_questions):
            input("\n⏸️  다음 예제로 진행하려면 Enter를 누르세요...")

def example_business_questions():
    """비즈니스 질문 예제"""
    print("💼 비즈니스 질문 예제")
    print("=" * 40)
    
    chatbot = NovaDualChatbot()
    
    business_questions = [
        "스타트업이 클라우드를 도입할 때 고려해야 할 요소는?",
        "디지털 트랜스포메이션의 핵심 전략은 무엇인가요?",
        "AI를 활용한 비즈니스 모델의 예시를 알려주세요."
    ]
    
    for i, question in enumerate(business_questions, 1):
        print(f"\n📝 예제 {i}: {question}")
        chatbot.chat(question)
        
        if i < len(business_questions):
            input("\n⏸️  다음 예제로 진행하려면 Enter를 누르세요...")

def example_custom_prompts():
    """커스텀 프롬프트 예제"""
    print("🎨 커스텀 프롬프트 예제")
    print("=" * 40)
    
    class CustomChatbot(NovaDualChatbot):
        def create_prompts(self, user_query: str):
            """커스텀 프롬프트 생성"""
            micro_prompt = f"""사용자 질문: "{user_query}"
            
간단하고 친근한 톤으로 "질문을 확인했어요! 자세한 답변을 준비 중입니다 😊" 스타일로 응답해주세요."""

            pro_prompt = f"""다음 질문에 대해 전문가의 관점에서 답변해주세요.
구체적인 예시와 실무 경험을 포함하여 설명해주세요.

질문: "{user_query}"

답변 구조:
1. 핵심 개념 설명
2. 실무 적용 사례
3. 주의사항 및 팁"""

            return micro_prompt, pro_prompt
    
    chatbot = CustomChatbot()
    question = "효과적인 코드 리뷰 방법을 알려주세요."
    
    print(f"📝 커스텀 프롬프트 테스트: {question}")
    chatbot.chat(question)

def main():
    """메인 실행 함수"""
    print("🚀 Amazon Nova 듀얼 모델 챗봇 - 사용 예제")
    print("=" * 60)
    
    examples = {
        "1": ("기술적 질문 예제", example_technical_questions),
        "2": ("비즈니스 질문 예제", example_business_questions),
        "3": ("커스텀 프롬프트 예제", example_custom_prompts)
    }
    
    print("실행할 예제를 선택하세요:")
    for key, (name, _) in examples.items():
        print(f"{key}: {name}")
    
    choice = input("\n선택 (1-3): ").strip()
    
    if choice in examples:
        name, func = examples[choice]
        print(f"\n🎯 {name} 실행")
        try:
            func()
        except Exception as e:
            print(f"❌ 예제 실행 중 오류: {e}")
            print("💡 먼저 'python test_nova_models.py'로 모델 접근 권한을 확인해보세요.")
    else:
        print("❌ 잘못된 선택입니다.")

if __name__ == "__main__":
    main()
