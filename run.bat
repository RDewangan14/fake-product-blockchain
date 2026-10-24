@echo off
echo ========================================================
echo   Fake Product Identification using Blockchain (TrustChain)
echo   SSIPMT Raipur - Dept. of Information Technology
echo ========================================================
echo.
echo Installing any missing packages...
python -m pip install -r requirements.txt
echo.
echo Seeding initial blockchain data if not present...
python seed_data.py
echo.
echo Starting Web Server at http://localhost:5000 ...
python app.py
pause
