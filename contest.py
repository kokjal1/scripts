
from bs4 import BeautifulSoup as BS
import requests
import os
import sys


def get_html(url):
    return requests.get(url).content


def get_problems(contest_id):
    url = 'http://codeforces.com/contest/'
    sp = BS(get_html(url + contest_id), 'html.parser')
    table = sp.select("table.problems")[0]
    trs = table.select("tr")
    
    res = {"names" : [], "links" : []}

    for tr in trs[1:]:
        td = tr.select("td")[0]
        a = td.find("a")
        res["names"].append(a.text.strip().lower())
        res["links"].append('http://codeforces.com' + a.attrs.get("href"))

    return res


def make_templates(contest_id, problems_names):
    if os.path.exists(contest_id):
        os.system("rm -r {}".format(contest_id))
    os.system("mkdir {}".format(contest_id))
    from os.path import expanduser
    home = expanduser("~")
    tpl = open("{}/Desktop/cpp_codes/main.cpp".format(home), "r").read()
    for problem in problems_names:
        os.system("mkdir {}/{}".format(contest_id, problem))
        tpl_file = open("{}/{}/{}.cpp".format(contest_id, problem, problem), "w")
        tpl_file.write(tpl)
        tpl_file.close()


def make_tests(contest_id, problems):
    res = {}
    res2 = {}
    for problem in problems["names"]:
        res[problem] = []
        res2[problem] = []

    for i in range(len(problems["names"])):

        sp = BS(get_html(problems["links"][i]), "html.parser")
        stests = sp.select("div.sample-tests")[0]

        tp = "input"
        for it in range(2):
            inputs = stests.select(".{}".format(tp))

            for inp in inputs:
                pre = inp.find("pre")
                res[problems["names"][i]].append(pre.text)

            tp = "output"
            res, res2 = res2, res

    for i in range(len(problems["names"])):
        name = problems["names"][i]
        tp = "in"

        for i in range(2):
            test = 0
            for case in res[name]:

                inp_file = open("{}/{}/{}{}".format(contest_id, name, tp, str(test)), "w")
                inp_file.write(case)
                inp_file.close()
                test += 1

            tp = "out"
            res, res2 = res2, res

def make_testers(contest_id, problems_names):
    from os.path import expanduser
    home = expanduser("~")
    tester = open("{}/Desktop/scripts/tester.py".format(home), "r").read()
    for problem_name in problems_names:
        tester_file = open("{}/{}/test".format(contest_id, problem_name), "w")
        new_tester = tester
        new_tester = new_tester.replace("TASK", problem_name + ".cpp")
        new_tester = new_tester.replace("EXE", problem_name)
        tester_file.write(new_tester)
        tester_file.close()
        os.system("chmod +x {}/{}/test".format(contest_id, problem_name))


def main():
    contest_id = sys.argv[1]
    problems = get_problems(contest_id)
    make_templates(contest_id, problems['names'])
    make_tests(contest_id, problems)
    make_testers(contest_id, problems["names"])
    

main()
