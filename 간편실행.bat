@echo off
chcp 65001 > nul
echo ========================================
echo 🚀 키워드 추천 시스템 - 간편 실행
echo ========================================
echo.

echo 패키지 설치 중...
python -m pip install streamlit pandas requests --quiet --upgrade

echo.
echo 앱 실행 중...
echo 브라우저가 자동으로 열립니다!
echo.

python -m streamlit run keyword_finder_improved.py

pause
