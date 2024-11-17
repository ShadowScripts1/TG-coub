Here’s the cleaned-up version of your README:

---

# TG-coub  
AUTO CLAIM FOR COUB / @coub  

[![Join our Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/shadowscripters)  
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ShadowScripts1)  

---

## Table of Contents
- [Warning](#warning)  
- [Registration](#registration)  
- [How to Use](#how-to-use)  
  - [Windows](#windows)  
  - [Linux](#linux)  
  - [Termux](#termux)  
- [How to Get tgWebAppData](#how-to-get-tgwebappdata-query_id--user_id)  
- [Support Me](#support-me)  
- [Contact](#contact)  

---

## Warning  
**All risks are borne by the user.**  

---

## Registration  
Click the following link to register:  
[https://t.me/coubCryptoBot/](https://t.me/coub/app?startapp=coub__marker_18417712)  

---

## How to Use  

### Windows  
1. Ensure Python (version 3.8 or newer) and Git are installed:  
   - [Python](https://python.org)  
   - [Git](https://git-scm.com/)  

2. Clone this repository:  
   ```bash
   git clone https://github.com/ShadowScripts1/TG-coub
   ```

3. Navigate to the folder:  
   ```bash
   cd TG-coub
   ```

4. Install required dependencies:  
   ```bash
   python -m pip install -r requirements.txt
   ```

5. Edit `data.txt`, entering query data. Each line corresponds to one account.  

6. Run the script:  
   ```bash
   python bot.py
   ```

### Linux  
1. Install Python (3.8 or newer) and Git:  
   ```bash
   sudo apt install python3 python3-pip git
   ```

2. Clone the repository:  
   ```bash
   git clone https://github.com/ShadowScripts1/TG-coub
   ```

3. Navigate to the folder:  
   ```bash
   cd TG-coub
   ```

4. Install dependencies:  
   ```bash
   python -m pip install -r requirements.txt
   ```

5. Edit `data.txt` with query data, one line per account.  

6. Run the script:  
   ```bash
   python bot.py
   ```

### Termux  
1. Install Python (3.8 or newer) and Git:  
   ```bash
   pkg install python3 git
   ```

2. Clone the repository:  
   ```bash
   git clone https://github.com/ShadowScripts1/TG-coub
   ```

3. Navigate to the folder:  
   ```bash
   cd TG-coub
   ```

4. Install dependencies:  
   ```bash
   python -m pip install -r requirements.txt
   ```

5. Edit `data.txt`, adding one line per account.  

6. Run the script:  
   ```bash
   python bot.py
   ```

---

## How to Get tgWebAppData (query_id / user_id)  
1. Log in to Telegram via the portable or web version.  
2. Launch the bot.  
3. Open the console by pressing **F12**.  
4. Enter the following code to retrieve the data:  
   ```javascript
   copy(Telegram.WebApp.initData)
   ```
5. The output will look like:  
   ```
   query_id=AA....
   user=%7B%22id%....
   ```

6. Add the data to the `data.txt` file. For multiple accounts, add each query ID on a new line:  
   ```txt
   query_id=xxxxxxxxx-Rxxxxujhash=cxxx
   query_id=xxxxxxxxx-Rxxxxujhash=cxxxx
   ```

---

## Support Me  
If you find this tool useful, consider supporting me:  

- **EVM:** `0x7BeE9994a631523e22A3aB83039c196bFc6BC513`  
- **Solana:** `6mbFy6AojWo3J5ksa1SYHHyCWw5Bms4p9McKmaFkCsyW`  

---

## Contact  
For questions or support, join: [Scripters Enclave chat](https://t.me/chatwithscripters)  

---

**Thank you!**