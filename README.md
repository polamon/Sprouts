# Sprouts

Gather new posts from 1point3acres bbs and store summaries in Google Sheet or local csv file.  
从一亩三分地论坛获取新帖，将摘要存入Google Sheets或本地csv文件。

## Installation
``` shell
pip3 install -r requirements.txt
```

操作Google Sheets需开启Google Sheets API和下载client_secret.json，请参考[Turn on the Google Sheets API](https://developers.google.com/sheets/api/quickstart/python)获取。

## Usage

### Exampel 1
将论坛前5页，发帖时间在一周内的Intern面经存入指定的Google Sheets：
``` shell
python3 sprouts/main.py --page_number 5 --max_age 7 \
      --work_type Intern \
      --gsheet_id [GOOGLE SHEETS ID]
```
![example 2](images/google_sheets.png)

### Example 2
将论坛前5页，发帖时间在一周内的Google全职面经存入Google.csv，帖子链接使用TinyURL短网址：

``` shell
python3 sprouts/main.py --page_number 5 --max_age 7 \
    --company Google --work_type Fulltime  \
    --csv_file Google.csv \
    --use_shortened_url
```

![example 1](images/local_csv.png)


关于其他参数：
```
python3 sprouts/main.py --help
```
