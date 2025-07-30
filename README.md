# Amazon Nova Dual Model Chatbot 🤖

Nova Micro와 Nova Pro를 조합하여 **빠른 초기 응답**과 **상세한 최종 답변**을 제공하는 혁신적인 듀얼 모델 챗봇입니다.

## 🚀 주요 특징

- **⚡ 즉각적인 응답**: Nova Micro가 1초 이내에 초기 응답 제공
- **🧠 고품질 답변**: Nova Pro가 상세하고 정확한 최종 답변 생성
- **🔄 병렬 처리**: 두 모델을 동시에 호출하여 지연 시간 최소화
- **📡 실시간 스트리밍**: 타이핑 효과로 자연스러운 대화 경험
- **💰 비용 효율성**: 질문당 약 $0.0016 (약 0.2원) 수준

## 🎯 아키텍처 개념

이 프로젝트는 **"지연-품질 상충 관계"**를 해결하는 혁신적인 접근법을 구현합니다:

1. **Nova Micro (단거리 주자)**: 즉각적인 초기 응답으로 사용자 대기 시간 최소화
2. **Nova Pro (장거리 주자)**: 백그라운드에서 심층적인 최종 답변 생성
3. **병렬 스트리밍 오케스트레이션**: 두 모델을 동시에 호출하여 자연스러운 연속 답변 제공

```
사용자 질문 → [Nova Micro] ──┐
            ↘ [Nova Pro]  ──┘ → 연속 스트리밍 답변
```

### 🔄 병렬 스트리밍 프로세스
1. **동시 호출**: 질문 입력 시 두 모델을 병렬로 호출
2. **Micro 스트리밍**: Nova Micro가 즉시 간결한 답변을 스트리밍 출력
3. **Pro 버퍼링**: Nova Pro 결과를 백그라운드에서 버퍼에 수집
4. **자연스러운 연결**: Micro 완료 후 Pro 답변이 자연스럽게 이어짐
5. **하나의 답변**: 사용자는 하나의 AI가 점진적으로 상세해지는 것으로 인식

## 📋 사전 요구사항

### 1. Python 환경
```bash
python --version  # Python 3.8 이상 필요
```

### 2. AWS 자격 증명 설정
다음 중 하나의 방법으로 AWS 자격 증명을 설정하세요:

#### 방법 1: AWS CLI 사용
```bash
pip install awscli
aws configure
```

#### 방법 2: 환경 변수 설정
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

#### 방법 3: ~/.aws/credentials 파일 생성
```ini
[default]
aws_access_key_id = your_access_key
aws_secret_access_key = your_secret_key
region = us-east-1
```

### 3. Bedrock 모델 접근 권한 활성화

⚠️ **중요**: AWS Management Console에서 Nova 모델 접근 권한을 활성화해야 합니다.

1. AWS Console → Amazon Bedrock 서비스 이동
2. 왼쪽 메뉴에서 "Model access" 선택
3. "Manage model access" 버튼 클릭
4. 다음 모델들을 체크하고 저장:
   - ✅ Amazon Nova Micro
   - ✅ Amazon Nova Pro

## 🛠️ 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/amazon-nova-dual-chatbot.git
cd amazon-nova-dual-chatbot
```

### 2. 가상 환경 생성 (권장)
```bash
python -m venv nova_chatbot_env
source nova_chatbot_env/bin/activate  # macOS/Linux
# 또는
nova_chatbot_env\Scripts\activate     # Windows
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 모델 접근 권한 테스트
```bash
python test_nova_models.py
```

### 5. 챗봇 실행
```bash
python nova_dual_chatbot.py
```

### 6. 간단 테스트 (권장)
```bash
python quick_test.py
```

## 🎮 사용 방법

실행하면 두 가지 모드를 선택할 수 있습니다:

### 모드 1: 대화형 모드
- 직접 질문을 입력하여 챗봇과 대화
- `quit` 또는 `exit` 입력으로 종료

### 모드 2: 테스트 모드
- 미리 준비된 4개의 테스트 질문으로 성능 확인
- 각 질문마다 Nova Micro와 Nova Pro의 응답 시간 비교 가능

## 📊 실행 결과 예시

```
💬 질문: AWS Lambda와 EC2의 차이점을 설명해주세요.
============================================================
🤖 답변:
🏃‍♀️ Nova Pro 스트리밍 시작...
🏃‍♂️ Nova Micro 스트리밍 시작...

AWS Lambda와 EC2는 모두 AWS의 컴퓨팅 서비스이지만 운영 방식에서 큰 차이가 있습니다. 
Lambda는 서버리스 컴퓨팅으로 코드만 업로드하면 AWS가 모든 인프라를 관리하며, 
EC2는 가상 서버를 직접 관리해야 합니다. 더 구체적으로 살펴보겠습니다.

## AWS Lambda vs EC2 상세 비교

더 구체적으로 살펴보면, 두 서비스는 각각 다른 사용 사례와 장단점을 가지고 있습니다...

[실시간으로 타이핑되는 상세한 답변이 자연스럽게 이어짐]
```

## 📁 프로젝트 구조

```
amazon-nova-dual-chatbot/
├── README.md                    # 프로젝트 설명서
├── requirements.txt             # Python 의존성
├── nova_dual_chatbot.py        # 메인 챗봇 애플리케이션
├── test_nova_models.py         # 모델 접근 권한 테스트
├── single_test.py              # 단일 질문 테스트
├── examples/                   # 사용 예제
│   └── example_usage.py
└── docs/                       # 추가 문서
    ├── ARCHITECTURE.md         # 아키텍처 상세 설명
    └── TROUBLESHOOTING.md      # 문제 해결 가이드
```

## 🔧 커스터마이징

### 프롬프트 수정
`create_prompts()` 메서드에서 각 모델의 프롬프트를 수정할 수 있습니다:

```python
def create_prompts(self, user_query: str):
    micro_prompt = f"""당신만의 초기 응답 스타일..."""
    pro_prompt = f"""당신만의 상세 답변 스타일..."""
    return micro_prompt, pro_prompt
```

### 모델 파라미터 조정
각 모델의 `inferenceConfig`에서 파라미터를 조정할 수 있습니다:

```python
"inferenceConfig": {
    "max_new_tokens": 100,    # 생성할 최대 토큰 수
    "temperature": 0.3        # 창의성 수준 (0.0-1.0)
}
```

## 🐛 문제 해결

### 1. 모델 접근 권한 오류
```
AccessDeniedException: You don't have access to the model
```
→ AWS Console에서 Bedrock 모델 접근 권한을 활성화하세요.

### 2. 자격 증명 오류
```
NoCredentialsError: Unable to locate credentials
```
→ AWS 자격 증명을 올바르게 설정했는지 확인하세요.

### 3. 리전 오류
```
Could not connect to the endpoint URL
```
→ 코드의 `region` 파라미터를 사용 가능한 리전으로 변경하세요.

## 📚 참고 자료

- [Amazon Bedrock 사용자 가이드](https://docs.aws.amazon.com/bedrock/)
- [Nova 모델 문서](https://docs.aws.amazon.com/bedrock/latest/userguide/nova-models.html)
- [Boto3 Bedrock Runtime 문서](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime.html)
