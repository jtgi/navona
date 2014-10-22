import mechanize
import cookielib
import urllib
import logging
import sys
import requests
import json
import re

def main(argv):
    class_id = "hzhggjui1ld2gc" #cs311
    wolframs_uid = "h1v2rdkcvmht6" #steve_wolfram's uid
    bonus_points = 0;
    
    credentials = get_credentials(argv)
    session = get_session(credentials)
    threads = get_thread_listing(session, class_id) 

    for thread_meta in threads:
      tid = thread_meta["id"]
      thread = get_thread(session, tid, class_id)
      bonus_points += count_bonus_points(thread, wolframs_uid)

    sys.exit(bonus_points)


def get_credentials(argv):
  if len(argv) < 2:
    print 'navona.py username password'

  return argv

def get_thread(session, tid, class_id):
  url = "https://piazza.com/logic/api?method=content.get"

  payload = {
    'method': 'content.get',
    'params': {
      'nid': class_id,
      'cid': tid
    }
  }

  cookies = dict(piazza_session=session)
  r = requests.post(url, data=json.dumps(payload), cookies=cookies)

  result = r.json()
  return result["result"]


def count_bonus_points(thread, wolframs_uid):
  if not thread:
    return 0;

  points_found = 0
  stack = []
  stack.append(thread)

  while True:
    thread = stack.pop()

    if (("uid" in thread) and (thread["uid"] == wolframs_uid)) or (("type" in thread) and (thread["type"] == "i_answer")):
      if "history" in thread:
        points_found += extract_bonus_points(thread["history"][0]["content"])
      elif "subject" in thread:
        points_found += extract_bonus_points(thread["subject"])

    for t in thread["children"]:
      stack.append(t)

    if not stack:
      break;

  return points_found

def extract_bonus_points(str):
  bonus_points_strs = re.findall(r'[&#43;|\+](\d+)\s*BP[^\?]', str.encode("ascii", "ignore"))
  sum = 0

  for bp in bonus_points_strs:
    try:
      sum += int(bp)
    except ValueError:
      0 #do nothing but keep parsing

  return sum

def get_thread_listing(session, class_id):
    url = 'https://piazza.com/logic/api?method=network.get_my_feed'
    payload = { 
      'method': 'network.get_my_feed',
      'params': {
        "nid": class_id,
        "limit":2000,
        "sort":"updated"
      }
    }
    cookies = dict(piazza_session=session)

    r = requests.post(url, data=json.dumps(payload), cookies=cookies)
    threads = r.json()
    return threads["result"]["feed"]

def get_session(credentials):
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    br.set_handle_equiv(True)
    br.set_handle_gzip(False)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    r = br.open('https://piazza.com')
    html = r.read()

    br.select_form(nr=0)
    br["email"] = credentials[0]
    br["password"] = credentials[1]
    br.submit()

    return cj._cookies['piazza.com']['/']['piazza_session'].value

if __name__ == "__main__":
     main(sys.argv[1:])
