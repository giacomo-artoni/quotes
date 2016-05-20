#coding: utf8 
import datetime, sys
from selenium import webdriver

def main():
  Date = datetime.date.today()
  Path = '/home/artoni/public_html/quotes/original_pages/'
  browser = webdriver.PhantomJS()
  browser.get( 'https://www.ubs.com/global/it/quotes.html' ) 
  with open( Path + 'page_%s.txt' % Date, 'w' ) as text_file:
    text_file.write( browser.page_source.encode( 'utf-8' ) )
  browser.close()

if __name__ == '__main__':
  sys.exit( main() )
