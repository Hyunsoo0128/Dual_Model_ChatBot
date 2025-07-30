#!/usr/bin/env python3
"""
Nova 듀얼 챗봇 간단 테스트
병렬 스트리밍 기능 테스트용
"""

from nova_dual_chatbot import NovaDualChatbot
import sys

def main():
    print("🤖 Nova 듀얼 챗봇 간단 테스트")
    print("=" * 50)
    
    # 테스트 질문들
    test_questions = [
        "Python과 JavaScript의 차이점을 간단히 설명해주세요.",
        "AWS Lambda와 EC2의 차이점은 무엇인가요?",
        "머신러닝에서 오버피팅이란 무엇인가요?",
        "클라우드 컴퓨팅의 장점을 알려주세요."
    ]
    
    try:
        chatbot = NovaDualChatbot()
        
        # 사용자가 질문 선택하거나 직접 입력
        print("\n테스트 방법을 선택하세요:")
        print("1-4: 미리 준비된 테스트 질문")
        for i, question in enumerate(test_questions, 1):
            print(f"{i}: {question}")
        print("5: 직접 질문 입력")
        
        choice = input("\n선택 (1-5): ").strip()
        
        if choice in ['1', '2', '3', '4']:
            question = test_questions[int(choice) - 1]
            print(f"\n선택된 질문: {question}")
            chatbot.chat(question)
        elif choice == '5':
            question = input("\n질문을 입력하세요: ").strip()
            if question:
                chatbot.chat(question)
            else:
                print("❌ 질문이 입력되지 않았습니다.")
        else:
            print("❌ 잘못된 선택입니다.")
            
    except Exception as e:
        print(f"❌ 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
