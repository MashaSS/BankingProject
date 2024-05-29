# Test task for SimbirSoft

## Installation

1. Download project
```commandline
git clone https://github.com/MashaSS/BankingProject.git
cd BankingProject
```
2. Prepare environment 
```
pip install -r requirements.txt
```
3. Install java, download jar file for selenium (recommended 4.21) and run (in other cmd):
```
java -jar selenium-server-{your_version}.jar standalone
```
4. Paste url in `tests/config.ini` in `node_url` field.
```
[TestCapabilities]
node_url=http://localhost:4444/wd/hub
```
5. Run pytest by command:
```commandline
python .\tests\BankingProjectTests.py -s -v --alluredir=allure/
```
6. To see the allure report
```commandline
allure serve .\test\allure\ 
```