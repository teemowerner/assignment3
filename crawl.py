import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 기본 URL 설정
BASE_LIST_URL = "https://www.saramin.co.kr/zf_user/jobs/list/job-category?page={}"
BASE_DETAIL_URL = "https://www.saramin.co.kr/zf_user/jobs/relay/view?rec_idx={job_id}"


def fetch_job_listings():
    """
    Saramin 목록 페이지에서 Job ID를 수집
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.3 Safari/537.36"
    }

    job_ids = []

    for page in range(1, 6):  # 1~5페이지 크롤링
        url = BASE_LIST_URL.format(page)
        print(f"Fetching job list from: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch job list on page {page}: {e}")
            continue

        soup = BeautifulSoup(response.text, "lxml")
        job_cards = soup.find_all("a", href=True)

        for card in job_cards:
            href = card["href"]
            if "rec_idx=" in href:
                job_id = href.split("rec_idx=")[-1].split("&")[0]
                if job_id not in job_ids:
                    job_ids.append(job_id)

        print(f"Page {page}: Found {len(job_ids)} total job IDs so far")

    return job_ids


def fetch_job_details(job_id):
    """
    Saramin 상세 페이지에서 Job 정보를 가져오기
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.3 Safari/537.36"
    }

    try:
        response = requests.get(BASE_DETAIL_URL.format(job_id=job_id), headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        # HTML 저장 (디버깅용)
        with open(f"job_{job_id}.html", "w", encoding="utf-8") as file:
            file.write(response.text)

        details = {}

        # 회사명, 경력, 학력, 마감일
        description_meta = soup.find("meta", {"name": "description"})
        if description_meta:
            content = description_meta.get("content", "")
            content_parts = content.split(", ")
            details["company"] = content_parts[0] if len(content_parts) > 0 else "No Company"
            details["experience"] = content_parts[1] if len(content_parts) > 1 else "No Experience"
            details["education"] = content_parts[2] if len(content_parts) > 2 else "No Education"
            details["deadline"] = content_parts[4] if len(content_parts) > 4 else "No Deadline"

        # 홈페이지 URL
        website_meta = soup.find("meta", {"property": "og:url"})
        details["website"] = website_meta.get("content", "No Website Info") if website_meta else "No Website Info"

        # 제목
        title_tag = soup.find("title")
        details["title"] = title_tag.get_text(strip=True) if title_tag else "No Title Info"

        return details
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch job details for job ID {job_id}: {e}")
        return None


def fetch_job_details_selenium(job_id):
    """
    Saramin 상세 페이지에서 Selenium을 사용하여 Job 정보를 가져오기
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service("/path/to/chromedriver")  # ChromeDriver 경로 수정
    driver = webdriver.Chrome(service=service, options=options)

    try:
        url = BASE_DETAIL_URL.format(job_id=job_id)
        driver.get(url)
        time.sleep(3)  # JavaScript 렌더링 대기

        soup = BeautifulSoup(driver.page_source, "lxml")
        details = {}

        # 회사명, 경력, 학력, 마감일
        description_meta = soup.find("meta", {"name": "description"})
        if description_meta:
            content = description_meta.get("content", "")
            content_parts = content.split(", ")
            details["company"] = content_parts[0] if len(content_parts) > 0 else "No Company"
            details["experience"] = content_parts[1] if len(content_parts) > 1 else "No Experience"
            details["education"] = content_parts[2] if len(content_parts) > 2 else "No Education"
            details["deadline"] = content_parts[4] if len(content_parts) > 4 else "No Deadline"

        # 제목
        title_tag = soup.find("title")
        details["title"] = title_tag.get_text(strip=True) if title_tag else "No Title Info"

        return details
    finally:
        driver.quit()


def fetch_all_jobs():
    """
    모든 Job ID를 수집한 후 상세 데이터를 모두 가져오기
    """
    job_ids = fetch_job_listings()
    print(f"Found {len(job_ids)} total job IDs")

    jobs = []
    for i, job_id in enumerate(job_ids):
        print(f"Fetching details for job ID {job_id} ({i + 1}/{len(job_ids)})")
        job_details = fetch_job_details(job_id)
        if not job_details:  # requests 실패 시 Selenium으로 재시도
            print(f"Switching to Selenium for job ID {job_id}")
            job_details = fetch_job_details_selenium(job_id)
        if job_details:
            jobs.append(job_details)
        time.sleep(2)  # 요청 간 딜레이

    return jobs


if __name__ == "__main__":
    # 모든 공고 데이터 크롤링
    all_jobs = fetch_all_jobs()

    # JSON 파일로 저장
    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, ensure_ascii=False, indent=4)

    print(f"Total jobs fetched: {len(all_jobs)}")
    print("Jobs saved to jobs.json")
