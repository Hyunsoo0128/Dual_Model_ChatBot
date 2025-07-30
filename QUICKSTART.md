# 🚀 빠른 시작 가이드

Amazon Nova 듀얼 모델 챗봇을 5분 안에 실행해보세요!

## ⚡ 1분 체크리스트

- [ ] Python 3.8+ 설치됨
- [ ] AWS 계정 보유
- [ ] AWS 자격 증명 설정됨
- [ ] Bedrock Nova 모델 접근 권한 활성화됨

## 🏃‍♂️ 빠른 실행 (3단계)

### 1단계: 프로젝트 다운로드
```bash
git clone https://github.com/your-username/amazon-nova-dual-chatbot.git
cd amazon-nova-dual-chatbot
```

### 2단계: 환경 설정
```bash
# 가상 환경 생성 및 활성화
python -m venv nova_chatbot_env
source nova_chatbot_env/bin/activate  # macOS/Linux

# 의존성 설치
pip install -r requirements.txt
```

### 3단계: 실행!
```bash
# 모델 접근 권한 테스트
python test_nova_models.py

# 챗봇 실행
python nova_dual_chatbot.py
```

## 🔧 AWS 설정 (처음 사용자용)

### AWS 자격 증명 설정
```bash
# AWS CLI 설치 및 설정
pip install awscli
aws configure
```

### Bedrock 모델 접근 권한 활성화
1. [AWS Console](https://console.aws.amazon.com/) 로그인
2. **Amazon Bedrock** 서비스 이동
3. **Model access** → **Manage model access**
4. ✅ **Amazon Nova Micro** 체크
5. ✅ **Amazon Nova Pro** 체크
6. **Save changes** 클릭

## 🎯 첫 번째 테스트

```bash
# 단일 질문 테스트
python single_test.py
```

예상 결과:
```
🚀 [초기 응답 - Nova Micro]
💭 AWS Lambda의 주요 특징에 대해 상세히 설명해드리겠습니다!

📚 [상세 답변 - Nova Pro]
# AWS Lambda 주요 특징

## 1. 서버리스 컴퓨팅
AWS Lambda는 서버를 관리할 필요 없이...
[실시간 타이핑 효과로 상세한 답변 표시]
```

## 🎮 사용 모드

### 대화형 모드
```bash
python nova_dual_chatbot.py
# 1 선택 → 직접 질문 입력
```

### 테스트 모드
```bash
python nova_dual_chatbot.py
# 2 선택 → 미리 준비된 4개 질문 테스트
```

## 🐛 문제 발생 시

### 모델 접근 권한 오류
```
❌ AccessDeniedException: You don't have access to the model
```
→ AWS Console에서 Bedrock 모델 접근 권한 활성화 필요

### 자격 증명 오류
```
❌ NoCredentialsError: Unable to locate credentials
```
→ `aws configure` 명령으로 AWS 자격 증명 설정

### 상세한 문제 해결
📖 [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) 참조

## 💡 다음 단계

- 📚 [아키텍처 문서](docs/ARCHITECTURE.md) 읽기
- 🎨 [사용 예제](examples/example_usage.py) 실행
- 🔧 프롬프트 커스터마이징 시도
- 🌐 웹 애플리케이션으로 확장

## 🎉 성공!

챗봇이 정상 작동한다면 축하합니다! 
이제 Nova Micro의 빠른 응답과 Nova Pro의 고품질 답변을 동시에 경험할 수 있습니다.

---

⭐ 도움이 되었다면 GitHub에서 스타를 눌러주세요!
