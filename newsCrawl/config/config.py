import inspect
import os
from bs4 import BeautifulSoup
this_file=inspect.getfile(inspect.currentframe())
path=os.path.abspath(os.path.dirname(this_file))
try:
    txt=open(path+os.sep+"config",encoding='utf-8').read()
    soup=BeautifulSoup(txt,'lxml')

except:
    exit(0)
class all_rules:
    #读取起始URL
    urls=soup.urls.find_all("url")
    start_urls={}
    for url in urls:
        start_urls[url.web_name.string]=[]
        for start_url in url.start_urls.find_all("start_url"):
            start_urls[url.web_name.string].append(start_url.string)

    #读取title
    rules=soup.page_rules.title_rules.find_all("rules")
    rule_title={}
    for rule in rules:
        rule_title[rule.rules_id.string]={}
        rule_title[rule.rules_id.string]['xpath']=rule.rules_xpath.string
        rule_title[rule.rules_id.string]['regex']=rule.rules_regex.string
    #读取time
    rules=soup.page_rules.time_rules.find_all("rules")
    rule_time={}
    for rule in rules:
        rule_time[rule.rules_id.string]={}
        rule_time[rule.rules_id.string]['xpath'] = rule.rules_xpath.string
        rule_time[rule.rules_id.string]['regex'] = rule.rules_regex.string
        rule_time[rule.rules_id.string]['format'] = rule.rules_format.string

    #读取source
    rules = soup.page_rules.source_rules.find_all("rules")
    rule_source = {}
    for rule in rules:
        rule_source[rule.rules_id.string] = {}
        rule_source[rule.rules_id.string]['xpath'] = rule.rules_xpath.string
        rule_source[rule.rules_id.string]['regex'] = rule.rules_regex.string
    #读取img
    rules = soup.page_rules.img_rules.find_all("rules")
    rule_img = {}
    for rule in rules:
        rule_img[rule.rules_id.string] = {}
        rule_img[rule.rules_id.string]['xpath'] = rule.rules_xpath.string
        rule_img[rule.rules_id.string]['regex'] = rule.rules_regex.string
    #读取abstract
    rules = soup.page_rules.abstract_rules.find_all("rules")
    rule_abstract = {}
    for rule in rules:
        rule_abstract[rule.rules_id.string] = {}
        rule_abstract[rule.rules_id.string]['xpath'] = rule.rules_xpath.string
        rule_abstract[rule.rules_id.string]['regex'] = rule.rules_regex.string
    #读取type
    rules = soup.page_rules.type_rules.find_all("rules")
    rule_type = {}
    for rule in rules:
        rule_type[rule.rules_id.string] = {}
        rule_type[rule.rules_id.string]['xpath'] = rule.rules_xpath.string
        rule_type[rule.rules_id.string]['regex'] = rule.rules_regex.string
    #读取content
    rules=soup.page_rules.content_rules.find_all("rules")
    rule_content={}
    for rule in rules:
        rule_content[rule.rules_id.string]={}
        rule_content[rule.rules_id.string]['xpath'] = rule.rules_xpath.string
    #读取channel
    rules=soup.channel_rules.find_all("channels")
    channel={}
    for rule in rules:
        channel[rule.web_name.string]={}
        channel[rule.web_name.string]["channel"]={}
        channel[rule.web_name.string]["regex"] = {}
        for ch in rule.find_all("channel"):
            channel[rule.web_name.string]["channel"][ch.channel_word.string]=ch.channel_name.string
        for reg in rule.regexs.find_all('regex'):
            channel[rule.web_name.string]["regex"][reg.regex_id.string] = reg.regex_word.string

if __name__=='__main__':
    w=all_rules()
    # print(w.rule_content)