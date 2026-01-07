import streamlit as st
import time
import hmac
import hashlib
import base64
import requests
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="Naver Smart Keyword Finder", layout="wide")

# ========================================
# 🔑 여기에 당신의 API 정보를 입력하세요
# ========================================
MY_CUSTOMER_ID = "2431291"
MY_ACCESS_LICENSE = "01000000002f85b336dadb1e67413c8de445754d06663847264f1a1bf9c05c9154aa7c4158"
MY_SECRET_KEY = "AQAAAAAvhbM22tseZ0E8jeRFdU0GhyXivlCnGr9G/ya3y9Dayg=="
MY_SEARCH_CLIENT_ID = "NajLqImZF8USEmcyPoY7"
MY_SEARCH_CLIENT_SECRET = "MHcJY31Qeb"
# ========================================

# --- 네이버 API 관련 함수 ---
def generate_signature(timestamp, method, uri, secret_key):
    message = "{}.{}.{}".format(timestamp, method, uri)
    hash = hmac.new(secret_key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)
    return base64.b64encode(hash.digest()).decode('utf-8')

def get_keyword_data(hint_keyword, api_key, secret_key, customer_id):
    base_url = "https://api.searchad.naver.com"
    uri = "/keywordstool"
    timestamp = str(int(time.time() * 1000))
    signature = generate_signature(timestamp, "GET", uri, secret_key)

    headers = {
        "X-Timestamp": timestamp,
        "X-API-KEY": api_key,
        "X-Customer": str(customer_id),
        "X-Signature": signature,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/110.0.0.0 Safari/537.36"
    }
    params = {"hintKeywords": hint_keyword, "showDetail": "1"}

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(base_url + uri, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if 'keywordList' in data:
                    return data['keywordList']
                else:
                    st.warning(f"⚠️ 응답 형식이 예상과 다릅니다: {list(data.keys())}")
                    return None
            else:
                st.warning(f"⚠️ API 응답 코드: {response.status_code} (시도 {attempt+1}/{max_retries})")
                time.sleep(2)
                if attempt == max_retries - 1:
                    st.error(f"❌ API 요청 실패: {response.status_code}\n응답: {response.text[:200]}")
        except requests.exceptions.Timeout:
            st.warning(f"⏱️ 타임아웃 발생 (시도 {attempt+1}/{max_retries})")
            time.sleep(2)
            if attempt == max_retries - 1:
                st.error("❌ 서버 응답 시간 초과. 잠시 후 다시 시도해주세요.")
        except Exception as e:
            st.warning(f"⚠️ 에러 발생: {str(e)[:100]} (시도 {attempt+1}/{max_retries})")
            time.sleep(2)
            if attempt == max_retries - 1:
                st.error(f"❌ 접속 중 에러 발생: {e}")
    return None

def get_blog_competition(keyword, client_id, client_secret):
    try:
        url = "https://openapi.naver.com/v1/search/blog.json"
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }
        params = {"query": keyword, "display": 1}
        response = requests.get(url, headers=headers, params=params, timeout=5)

        if response.status_code == 200:
            return response.json().get('total', 0)
        else:
            # 디버깅을 위해 에러 로깅
            st.sidebar.caption(f"블로그 API 에러 ({keyword}): {response.status_code}")
    except Exception as e:
        st.sidebar.caption(f"블로그 API 예외 ({keyword}): {str(e)[:50]}")
    return 0

def get_shopping_competition(keyword, client_id, client_secret):
    try:
        url = "https://openapi.naver.com/v1/search/shop.json"
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }
        params = {"query": keyword, "display": 1}
        response = requests.get(url, headers=headers, params=params, timeout=5)

        if response.status_code == 200:
            return response.json().get('total', 0)
        else:
            st.sidebar.caption(f"쇼핑 API 에러 ({keyword}): {response.status_code}")
    except Exception as e:
        st.sidebar.caption(f"쇼핑 API 예외 ({keyword}): {str(e)[:50]}")
    return 0

# 🚨 [개선] 강화된 연관성 필터
def is_relevant(keyword, query):
    """검색어와 연관성 있는 키워드만 통과 (강화 버전)"""
    # 공백 제거 후 비교
    clean_keyword = keyword.replace(" ", "").lower()
    clean_query = query.replace(" ", "").lower()

    # 1. 검색어 전체가 포함되어 있으면 무조건 통과
    if clean_query in clean_keyword:
        return True

    # 2. 검색어를 토큰으로 분리
    query_tokens = [t for t in query.split() if len(t) > 1]  # 1글자 토큰 제외

    # 3. 최소 2개 이상의 토큰이 포함되어야 함 (검색어가 2개 이상의 토큰일 때)
    if len(query_tokens) >= 2:
        match_count = sum(1 for token in query_tokens if token in keyword)
        return match_count >= 2

    # 4. 단일 토큰이면 정확히 일치해야 함
    elif len(query_tokens) == 1:
        main_token = query_tokens[0]
        # 메인 토큰이 키워드에 포함되어 있으면 통과
        return main_token in keyword

    return False

def classify_keyword_intent(keyword, shopping_cnt, blog_cnt):
    purchase_signals = [
        '추천', '순위', 'best', '베스트', 'top', '인기', '가성비',
        '후기', '리뷰', '제품', '가격', '할인', '특가', '비교',
        '어떤거', '좋은', '괜찮은', '살까', '구매', '판매'
    ]

    info_signals = [
        '사용법', '방법', '관리', '청소', '세척', '보관', '수리',
        '원리', '작동', '차이', '뜻', '의미', '이란', '종류',
        '장단점', '단점', '문제', '고장', '해결', '팁', '주의사항'
    ]

    purchase_score = sum(1 for signal in purchase_signals if signal in keyword)
    info_score = sum(1 for signal in info_signals if signal in keyword)

    shopping_ratio = shopping_cnt / (blog_cnt + 1) if blog_cnt > 0 else 0

    if purchase_score > info_score or shopping_ratio > 0.5:
        return "구매확정"
    elif info_score > purchase_score:
        return "정보성"
    else:
        return "구매확정" if shopping_ratio > 0.2 else "정보성"

def calculate_purchase_score(row):
    search_volume = row['총검색량']
    blog_posts = row['블로그포스팅']
    shopping_ratio = row['쇼핑비율']
    comp_idx = row['경쟁수치']

    if blog_posts < 3000:
        blog_score = 10
    elif blog_posts < 10000:
        blog_score = 7
    elif blog_posts < 30000:
        blog_score = 5
    elif blog_posts < 100000:
        blog_score = 3
    else:
        blog_score = 1

    shopping_score = min(shopping_ratio / 10, 10)
    search_score = min(search_volume / 500, 10)
    ad_score = 4 - comp_idx

    total_score = (
        blog_score * 3 +
        shopping_score * 3 +
        search_score * 2 +
        ad_score * 1
    )

    return int(total_score)

def calculate_info_score(row):
    search_volume = row['총검색량']
    blog_posts = row['블로그포스팅']
    comp_idx = row['경쟁수치']

    if blog_posts < 5000:
        blog_score = 10
    elif blog_posts < 20000:
        blog_score = 8
    elif blog_posts < 50000:
        blog_score = 6
    elif blog_posts < 150000:
        blog_score = 4
    else:
        blog_score = 2

    if search_volume < 100:
        search_score = 1
    else:
        search_score = min(search_volume / 300, 10)

    ad_score = 4 - comp_idx

    total_score = (
        search_score * 4 +
        blog_score * 3 +
        ad_score * 1
    )

    return int(total_score)

def get_seasonality_bonus(keyword):
    current_month = datetime.now().month

    spring_keywords = ['봄', '꽃가루', '미세먼지', '환기']
    summer_keywords = ['여름', '에어컨', '선풍기', '제습', '냉감', '쿨링']
    fall_keywords = ['가을', '건조', '보습', '난방']
    winter_keywords = ['겨울', '히터', '온풍기', '가습기', '보온']

    season_map = {
        3: spring_keywords, 4: spring_keywords, 5: spring_keywords,
        6: summer_keywords, 7: summer_keywords, 8: summer_keywords,
        9: fall_keywords, 10: fall_keywords, 11: fall_keywords,
        12: winter_keywords, 1: winter_keywords, 2: winter_keywords
    }

    current_season_keywords = season_map.get(current_month, [])

    if any(season_word in keyword for season_word in current_season_keywords):
        return 1.3
    return 1.0

# --- UI 구성 ---
st.title("🎯 스마트 키워드 자동 추천 시스템")
st.markdown("**구매확정 + 정보성 키워드**를 최적 비율(3:7)로 자동 선별해드립니다.")

# 사이드바
with st.sidebar:
    st.header("⚙️ 추천 설정")

    purchase_count = st.number_input("구매확정 키워드 개수", 3, 10, 5,
                                     help="쇼핑커넥트용 키워드")
    info_count = st.number_input("정보성 키워드 개수", 5, 20, 10,
                                 help="저품질 방지용 키워드")

    min_search_volume = st.number_input("최소 검색량", 100, 5000, 500, step=100)

    # 🆕 연관성 필터 강도 설정
    st.divider()
    filter_strength = st.select_slider(
        "연관성 필터 강도",
        options=["약함", "보통", "강함"],
        value="보통",
        help="강함: 정확한 키워드만 | 보통: 균형잡힌 필터 | 약함: 넓은 범위"
    )

    st.divider()
    st.info("✅ API 정보가 코드에 저장되어 있습니다")
    st.success("✅ 강화된 연관성 필터")
    st.success("✅ 향상된 에러 로깅")

# 메인 화면
query = st.text_input("🔍 분석할 상품/카테고리를 입력하세요",
                     placeholder="예: 로봇청소기, 무선이어폰, 반려동물 사료")

if st.button("🚀 최적 키워드 자동 추천", use_container_width=True):
    if not query:
        st.warning("검색어를 입력해주세요.")
    else:
        with st.spinner('🤖 AI가 최적의 키워드를 찾고 있습니다...'):

            # 1단계: 기본 키워드 데이터
            raw_data = get_keyword_data(query, MY_ACCESS_LICENSE, MY_SECRET_KEY, MY_CUSTOMER_ID)

            if not raw_data:
                st.error("데이터를 가져오지 못했습니다. API 정보를 확인해주세요.")
                st.stop()

            if len(raw_data) == 0:
                st.warning("검색 결과가 없습니다. 다른 키워드로 시도해주세요.")
                st.stop()

            df = pd.DataFrame(raw_data)

            # 기본 전처리 (안전한 변환)
            df['PC'] = pd.to_numeric(df.get('monthlyPcQcCnt', 0), errors='coerce').fillna(0).astype(int)
            df['모바일'] = pd.to_numeric(df.get('monthlyMobileQcCnt', 0), errors='coerce').fillna(0).astype(int)
            df['총검색량'] = df['PC'] + df['모바일']

            # ==========================================================
            # 🚨 [개선] 강화된 연관성 필터
            # ==========================================================
            original_count = len(df)

            # relKeyword 컬럼 확인
            if 'relKeyword' not in df.columns:
                st.error("❌ API 응답에 'relKeyword' 필드가 없습니다.")
                st.write("사용 가능한 필드:", list(df.columns))
                st.stop()

            # 필터 적용 (필터 강도에 따라 다르게 적용)
            if filter_strength == "강함":
                # 검색어 전체가 포함된 키워드만
                clean_query = query.replace(" ", "").lower()
                df = df[df['relKeyword'].apply(lambda x: clean_query in x.replace(" ", "").lower())].copy()
            else:
                # 기본 연관성 필터
                df = df[df['relKeyword'].apply(lambda x: is_relevant(x, query))].copy()

            filtered_count = len(df)

            if original_count > filtered_count:
                st.toast(f"🧹 연관성 낮은 키워드 {original_count - filtered_count}개를 필터링했습니다!")
            # ==========================================================

            # compIdx 매핑
            comp_map = {'LOW': 1, '낮음': 1, 'MEDIUM': 2, '중간': 2, 'HIGH': 3, '높음': 3}
            df['경쟁수치'] = df['compIdx'].map(comp_map).fillna(3).astype(int)

            # 필터링
            df = df[df['총검색량'] >= min_search_volume].copy()

            if len(df) == 0:
                st.warning("검색량 조건을 만족하는 키워드가 없습니다. 최소 검색량을 낮춰보세요.")
                st.stop()

            st.info(f"📊 분석 대상 키워드: {len(df)}개")

            # 2단계: 블로그/쇼핑 데이터 수집
            progress_bar = st.progress(0)
            status_text = st.empty()

            blog_counts = []
            shopping_counts = []

            # API 호출 제한을 고려한 배치 처리
            batch_size = 50  # 한 번에 최대 50개만 처리
            total_keywords = len(df)

            if total_keywords > batch_size:
                st.warning(f"⚠️ 키워드가 {total_keywords}개로 많습니다. 상위 {batch_size}개만 분석합니다.")
                df = df.head(batch_size)

            for idx, keyword in enumerate(df['relKeyword']):
                status_text.text(f"키워드 분석 중... {idx+1}/{len(df)}: {keyword}")
                progress_bar.progress((idx + 1) / len(df))

                blog_cnt = get_blog_competition(keyword, MY_SEARCH_CLIENT_ID, MY_SEARCH_CLIENT_SECRET)
                shopping_cnt = get_shopping_competition(keyword, MY_SEARCH_CLIENT_ID, MY_SEARCH_CLIENT_SECRET)

                blog_counts.append(blog_cnt)
                shopping_counts.append(shopping_cnt)

                # API 호출 간격
                time.sleep(0.4)

            progress_bar.empty()
            status_text.empty()

            df['블로그포스팅'] = blog_counts
            df['쇼핑상품수'] = shopping_counts
            df['쇼핑비율'] = (df['쇼핑상품수'] / (df['블로그포스팅'] + 1) * 100).round(1)

            # 3단계: 키워드 자동 분류
            status_text.text("🎯 키워드 유형을 분류하는 중...")

            df['키워드타입'] = df.apply(
                lambda x: classify_keyword_intent(x['relKeyword'], x['쇼핑상품수'], x['블로그포스팅']),
                axis=1
            )

            # 4단계: 타입별 점수 계산
            df['계절보너스'] = df['relKeyword'].apply(get_seasonality_bonus)

            def calculate_final_score(row):
                if row['키워드타입'] == '구매확정':
                    return int(calculate_purchase_score(row) * row['계절보너스'])
                else:
                    return int(calculate_info_score(row) * row['계절보너스'])

            df['최종점수'] = df.apply(calculate_final_score, axis=1)

            # 5단계: 최적 키워드 선별
            purchase_df = df[df['키워드타입'] == '구매확정'].sort_values('최종점수', ascending=False).head(purchase_count)
            info_df = df[df['키워드타입'] == '정보성'].sort_values('최종점수', ascending=False).head(info_count)

            status_text.empty()

            # 결과 출력
            st.success(f"✨ '{query}' 최적 키워드 조합 완성!")

            # 요약 메트릭
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("구매확정 키워드", f"{len(purchase_df)}개",
                         help="쇼핑커넥트 포스팅용")
            with col2:
                st.metric("정보성 키워드", f"{len(info_df)}개",
                         help="저품질 방지용")
            with col3:
                ratio = f"{len(purchase_df)}:{len(info_df)}"
                st.metric("포스팅 비율", ratio,
                         help="권장: 3:7 ~ 4:6")
            with col4:
                total_search = int(purchase_df['총검색량'].sum() + info_df['총검색량'].sum())
                st.metric("총 월검색량", f"{total_search:,}")

            # 구매확정 키워드
            st.subheader("🛒 구매확정 키워드 (쇼핑커넥트용)")
            st.caption("✅ 쇼핑성 높고 블로그 경쟁 낮은 키워드 - 수익화에 최적")

            if len(purchase_df) > 0:
                purchase_display = purchase_df[[
                    'relKeyword', '총검색량', '블로그포스팅', '쇼핑비율',
                    'compIdx', '최종점수'
                ]].copy()
                purchase_display.columns = ['키워드', '월검색량', '블로그수', '쇼핑성(%)', '광고경쟁', '점수']

                st.dataframe(
                    purchase_display,
                    use_container_width=True,
                    height=300
                )
            else:
                st.warning("구매확정 키워드를 찾지 못했습니다. 검색어를 바꿔보세요.")

            # 정보성 키워드
            st.subheader("📚 정보성 키워드 (저품질 방지용)")
            st.caption("✅ 검색량 있고 경쟁 낮은 키워드 - 블로그 신뢰도 구축")

            if len(info_df) > 0:
                info_display = info_df[[
                    'relKeyword', '총검색량', '블로그포스팅',
                    'compIdx', '최종점수'
                ]].copy()
                info_display.columns = ['키워드', '월검색량', '블로그수', '광고경쟁', '점수']

                st.dataframe(
                    info_display,
                    use_container_width=True,
                    height=400
                )
            else:
                st.warning("정보성 키워드를 찾지 못했습니다. 검색어를 바꿔보세요.")

            # 포스팅 전략 가이드
            st.divider()
            st.subheader("📝 추천 포스팅 전략")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🛒 구매확정 포스팅")
                if len(purchase_df) > 0:
                    for idx, row in purchase_df.head(3).iterrows():
                        st.markdown(f"**{row['relKeyword']}**")
                        st.caption(f"월 {int(row['총검색량']):,}회 검색 | 블로그 {int(row['블로그포스팅']):,}건")
                st.info("💡 쇼핑커넥트 링크 포함\n상품 비교/추천 콘텐츠")

            with col2:
                st.markdown("### 📚 정보성 포스팅")
                if len(info_df) > 0:
                    for idx, row in info_df.head(3).iterrows():
                        st.markdown(f"**{row['relKeyword']}**")
                        st.caption(f"월 {int(row['총검색량']):,}회 검색 | 블로그 {int(row['블로그포스팅']):,}건")
                st.info("💡 사용법/관리법 등\n순수 정보 제공 콘텐츠")

            # CSV 다운로드
            st.divider()
            col1, col2, col3 = st.columns(3)

            with col1:
                if len(purchase_df) > 0:
                    csv1 = purchase_df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        "📥 구매확정 키워드 다운로드",
                        csv1,
                        f"구매확정_{query}_{datetime.now().strftime('%Y%m%d')}.csv",
                        "text/csv"
                    )

            with col2:
                if len(info_df) > 0:
                    csv2 = info_df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        "📥 정보성 키워드 다운로드",
                        csv2,
                        f"정보성_{query}_{datetime.now().strftime('%Y%m%d')}.csv",
                        "text/csv"
                    )

            with col3:
                all_keywords = pd.concat([purchase_df, info_df])
                csv_all = all_keywords.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    "📥 전체 키워드 다운로드",
                    csv_all,
                    f"전체_{query}_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv"
                )

# 사용 가이드
with st.expander("📖 사용 가이드"):
    st.markdown("""
    ## 🎯 최적 키워드 선정 원리

    ### 강화된 연관성 필터 (IMPROVED!)
    - **보통 모드**: 검색어의 2개 이상 토큰이 포함된 키워드만 선별
    - **강함 모드**: 검색어 전체가 포함된 키워드만 선별
    - 예: "무선이어폰" 검색 시
      - ✅ 통과: "무선이어폰 추천", "블루투스 무선이어폰"
      - ❌ 제외: "무선청소기", "이어폰 케이스"

    ### 구매확정 키워드
    - 쇼핑성 높고 블로그 경쟁 낮은 키워드
    - 쇼핑커넥트 링크로 수익화

    ### 정보성 키워드
    - 검색량 있고 순수 정보 제공
    - 블로그 저품질 방지 및 신뢰도 구축

    ### 권장 포스팅 비율
    - 정보성 7 : 구매확정 3
    - 또는 정보성 6 : 구매확정 4

    ## 🛡️ 안정화 기능
    - User-Agent 추가로 차단 방지
    - Timeout 30초로 에러 방지
    - API 호출 간격 0.4초로 최적화
    - 배치 처리로 과도한 API 호출 방지
    - 향상된 에러 로깅 및 디버깅

    ## ⚠️ API 제한 사항
    - 네이버 API는 호출 횟수 제한이 있을 수 있습니다
    - 한 번에 50개 이상의 키워드는 처리하지 않습니다
    - 에러 발생 시 잠시 후 다시 시도해주세요
    """)

st.divider()
st.caption("🧹 강화된 연관성 필터 v2 | 🛡️ 향상된 안정성 | ✅ 배치 처리")
