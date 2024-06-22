import requests as r
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from io import StringIO
from db_con import *

URL = "https://static.sneedex.moe/"
TABLE_NAME = "ANIMES"


def get_html(url):
    opts = Options()
    driver = webdriver.Chrome()
    agent = driver.execute_script("return navigator.userAgent")
    opts.add_argument(f"user-agent={agent}")
    driver.get(url)
    html = driver.page_source
    driver.quit()
    return html


def get_table(soup):
    table_unfiltered = soup.select_one('table')
    return table_unfiltered


def pd_dataframe(table):
    dfs = pd.read_html(StringIO(str(table)))[0]
    return dfs


def update_db(df):
    cur, con = dbload()
    sqlquery = ""
    made_changes = False
    for index, row in df.iterrows():
        cur.execute("SELECT Title FROM ANIMES where Title=?", (row['Title'],))
        data = cur.fetchall()
        if not data:
            sqlquery = f"INSERT INTO {TABLE_NAME} (Title, Alias, Best, Alt, Notes, Comps) VALUES (?, ?, ?, ?, ?, ?)"
            data = (row['Title'], row['Alias'], row['Best'], row['Alt'], row['Notes'], row['Comps']) 
            cur.execute(sqlquery, data)
            con.commit()
            made_changes = True

    if made_changes:
        cur.execute("SELECT COUNT(*) as count_anime FROM ANIMES;")
        elements_in_db = cur.fetchone()[0]
        con.commit()
        print(f"Successfully updated the database, now with {elements_in_db} items!")
    else:
        print("The database is already updated")
    con_close(con)


def main():
    html = get_html(URL)
    html = BeautifulSoup(html, "html.parser")
    df = pd_dataframe(html)
    update_db(df)


if __name__ == '__main__':
    main()
