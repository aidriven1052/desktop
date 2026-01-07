@echo off
chcp 65001 > nul
echo ========================================
echo 🚀 네이버 키워드 추천 시스템 실행
echo ========================================
echo.

echo [1단계] 필수 패키지 설치 중...
pip install streamlit pandas requests
echo.

if %errorlevel% neq 0 (
    echo ❌ 패키지 설치 실패!
    echo 관리자 권한으로 실행하거나 다음 명령어를 시도하세요:
    echo pip install --user streamlit pandas requests
    pause
    exit /b 1
)

echo [2단계] Streamlit 앱 실행 중...
echo.
echo 🌐 브라우저가 자동으로 열립니다!
echo 📍 주소: http://localhost:8501
echo.
echo ⚠️ 종료하려면 Ctrl+C를 누르세요
echo.

streamlit run keyword_finder_improved.py

pause
