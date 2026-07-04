import os
import sys
from tavily import TavilyClient
from supabase import create_client, Client

# 환경 변수 로드
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not all([TAVILY_API_KEY, SUPABASE_URL, SUPABASE_KEY]):
    print("에러: 환경 변수(Secrets) 설정이 누락되었습니다.")
    sys.exit(1)

# 클라이언트 초기화
tavily = TavilyClient(api_key=TAVILY_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_and_save_news():
    print("🌐 테크 뉴스 수집 시작...")
    # Tavily를 통해 실리콘밸리 최신 테크 뉴스 검색
    response = tavily.search(
        query="Silicon Valley tech trends AI hiring news",
        search_depth="advanced",
        include_domains=["news.ycombinator.com", "techcrunch.com"],
        max_results=5
    )
    
    for result in response.get("results", []):
        try:
            supabase.table("tech_news").upsert({
                "url": result["url"],
                "title": result["title"],
                "content": result["content"],
                "source": "Tavily (News)"
            }).execute()
            print(f"저장 완료 (뉴스): {result['title']}")
        except Exception as e:
            print(f"뉴스 저장 건너뛰기 (중복 또는 에러): {e}")

def fetch_and_save_jobs():
    print("💼 채용 공고 데이터 수집 시작...")
    response = tavily.search(
        query="Software Engineer Tech Job openings 2026",
        search_depth="advanced",
        include_domains=["github.com", "crunchbase.com", "adzuna.com"],
        max_results=5
    )
    
    for result in response.get("results", []):
        try:
            supabase.table("job_postings").upsert({
                "url": result["url"],
                "title": result["title"],
                "company": "데이터 소스 참조",
                "content": result["content"],
                "source": "Tavily (Job)"
            }).execute()
            print(f"저장 완료 (공고): {result['title']}")
        except Exception as e:
            print(f"공고 저장 건너뛰기 (중복 또는 에러): {e}")

if __name__ == "__main__":
    fetch_and_save_news()
    fetch_and_save_jobs()
    print("🎉 모든 데이터 수집 및 Supabase 적재 완료!")
