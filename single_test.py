#!/usr/bin/env python3
"""
단일 질문으로 듀얼 모델 테스트

이 스크립트는 하나의 질문으로 Nova 듀얼 모델 챗봇의
동작을 빠르게 테스트할 수 있습니다.
"""

from nova_dual_chatbot import NovaDualChatbot

def main():
    print("🤖 Amazon Nova 듀얼 모델 챗봇 - 단일 테스트")
    print("=" * 60)
    
    try:
        # 챗봇 인스턴스 생성
        chatbot = NovaDualChatbot()
        
        # 테스트 질문
        test_query = "AWS Lambda의 주요 특징 3가지를 설명해주세요."
        
        print(f"📝 테스트 질문: {test_query}")
        print()
        
        # 챗봇 실행
        chatbot.chat(test_query)
        
        print("\n🎉 단일 테스트 완료!")
        print("💡 전체 기능을 테스트하려면 'python nova_dual_chatbot.py'를 실행하세요.")
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류 발생: {e}")
        print("💡 먼저 'python test_nova_models.py'로 모델 접근 권한을 확인해보세요.")

if __name__ == "__main__":
    main()
