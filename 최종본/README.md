🚀 실행 가이드

1. Python 환경 준비

# 가상환경 생성 (선택)
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# pip 최신화
pip install -U pip


2. 패키지 설치
pip install -r requirements.txt


3. API 키 설정
	•	필수: OpenAI API Key
	•	선택: SERPAPI_API_KEY, BING_API_KEY

설정 방법:
# 터미널에서
export OPENAI_API_KEY="sk-..."        # macOS/Linux
setx OPENAI_API_KEY "sk-..."          # Windows

# 또는 .env 파일 생성
OPENAI_API_KEY=sk-xxxx
SERPAPI_API_KEY=your-serpapi-key
BING_API_KEY=your-bing-key
Streamlit 사이드바에서도 직접 입력 가능하므로 .env는 선택사항입니다.


4. CSV 데이터 준비

해당 코드는 /mnt/data 또는 현재 프로젝트 루트(./)에 아래 CSV 파일이 있을 때 더 풍부한 분석을 제공합니다.
	•	job_market.csv
	•	macro_indicators.csv
	•	skills_analysis.csv
	•	tech_trends.csv

없어도 실행은 가능하지만, 일부 기능(스킬 매칭, 채용 트렌드 시각화 등)이 비활성화됩니다.


5. 실행하기
streamlit run app.py
실행 후 브라우저에서 http://localhost:8501 자동 접속됩니다.

🧭 사용 흐름 요약
	1.	💬 대화 탭: 일반 코칭 대화, 파일(txt/docx) 업로드 후 첨삭 가능
	2.	🧭 자소서 평가 탭: 규칙 기반 점수 + LLM 개선안 + 스킬 매칭
	3.	📈 트렌드/기업 탭: CSV 기반 시각화 + 웹 리서치(기업 인재상, 기술 수요)
	4.	사이드바: 모델 선택, 톤/길이 조절, 내보내기 옵션(PDF, Word, TXT, HTML)
