"""
Flask를 사용해 잡 스크래퍼의 프론트엔드를 구축합니다.
유저는 python, javascript, java 등과 같은 용어를 검색할 수 있어야 합니다.
스크래퍼는 berlinstartupjobs.com, weworkremotely.com 및 web3.career의 결과를 표시해야 합니다.
우리는 이미 berlinstartupjobs.com 스크래퍼에 대한 코드가 있으므로 weworkremotely.com 및 web3.career를 스크래핑하는 코드를 작성해야 합니다.

검색 URL은 다음과 같습니다:
https://berlinstartupjobs.com/skill-areas// where <s> is the search term (i.e https://berlinstartupjobs.com/skill-areas/python/)

https://web3.career/-jobs where <s> is the search term (i.e https://web3.career/python-jobs)

https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term= where <s> is the search term (i.e https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term=python)
"""

"""
output
1. 스크랩할 사이트 선택
    1. berlinstartupjobs
        1. 검색할 직업 입력
        2. 스크랩
        3. 스크랩 결과 리스트 출력
        4. csv로 다운로드 버튼
        5. 홈화면으로 돌아가기
    2. weworkremotely
        1. 검색할 직업 입력
        2. 스크랩
        3. 스크랩 결과 리스트 출력
        4. csv로 다운로드 버튼
        5. 홈화면으로 돌아가기
    3. web3.career
        1. 검색할 직업 입력
        2. 스크랩
        3. 스크랩 결과 리스트 출력
        4. csv로 다운로드 버튼
        5. 홈화면으로 돌아가기
"""

from flask import Flask, render_template, request, redirect, send_file
from scrape import berlinstartupScrape, weworkremotelyScrape, web3careerScrape

app = Flask(__name__)

db = {
    'berlin': {},
    'web3': {},
    'wework': {}
}

brscraper = berlinstartupScrape()
w3scraper = web3careerScrape()
rmscraper = weworkremotelyScrape()


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search_berlinstartupjobs")
def search_berlinstartupjobs():
    return render_template('search_berlinstartupjobs.html')

@app.route("/result_berlinstartupjobs")
def result_berlinstartupjobs():
    keyword = request.args.get("keyword")
    if keyword == "":
        return redirect("/search_berlinstartupjobs")
    if keyword in db['berlin']:
        jobs = db['berlin'][keyword]
    else:
        jobs = brscraper.br_Scrape(keyword)
        db['berlin'][keyword] = jobs
    return render_template('result_berlinstartupjobs.html', keyword = keyword, jobs = jobs)

@app.route("/export_berlinstartupjobs")
def export_berlinstartupjobs():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/search_berlinstartupjobs")
    if keyword not in db['berlin']:
        return redirect(f"/result_berlinstartupjobs?keyword={keyword}")
    brscraper.to_csv(keyword, db['berlin'][keyword])
    return send_file(f"{keyword}_berlinstartup.csv", as_attachment=True)

@app.route("/search_web3career")
def search_web3career():
    return render_template('search_web3career.html')

@app.route("/result_web3career")
def result_web3career():
    keyword = request.args.get("keyword")
    if keyword == "":
        return redirect("/search_web3career")
    if keyword in db['web3']:
        jobs = db['web3'][keyword]
    else:
        jobs = w3scraper.w3_Scrape_pages(keyword)
        db['web3'][keyword] = jobs
    return render_template('result_web3career.html', keyword = keyword, jobs = jobs)

@app.route("/export_web3career")
def export_web3career():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/search_web3career")
    if keyword not in db['web3']:
        return redirect(f"/result_web3career?keyword={keyword}")
    w3scraper.to_csv(keyword, db['web3'][keyword])
    return send_file(f"{keyword}_web3career.csv", as_attachment=True)

@app.route("/search_weworkremotely")
def search_weworkremotely():
    return render_template('search_weworkremotely.html')

@app.route("/result_weworkremotely")
def result_weworkremotely():
    keyword = request.args.get("keyword")
    if keyword == "":
        return redirect("/search_weworkremotely")
    if keyword in db['wework']:
        jobs = db['wework'][keyword]
    else:
        jobs = rmscraper.rm_Scrape(keyword)
        db['wework'][keyword] = jobs
    return render_template('result_weworkremotely.html', keyword = keyword, jobs = jobs)

@app.route("/export_weworkremotely")
def export_weworkremotely():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/search_weworkremotely")
    if keyword not in db['wework']:
        return redirect(f"/result_weworkremotely?keyword={keyword}")
    rmscraper.to_csv(keyword, db['wework'][keyword])
    return send_file(f"{keyword}_weworkremotely.csv", as_attachment=True)

@app.route("/static/berlin/<keyword>")
def static_berlin_result(keyword):
    keyword = (keyword or "").strip()
    if not keyword:
        return redirect("/search_berlinstartupjobs")
    if keyword in db['berlin']:
        jobs = db['berlin'][keyword]
    else:
        jobs = brscraper.br_Scrape(keyword)
        db['berlin'][keyword] = jobs
    return render_template('result_berlinstartupjobs.html', keyword=keyword, jobs=jobs)

@app.route("/static/web3/<keyword>")
def static_web3_result(keyword):
    keyword = (keyword or "").strip()
    if not keyword:
        return redirect("/search_web3career")
    if keyword in db['web3']:
        jobs = db['web3'][keyword]
    else:
        jobs = w3scraper.w3_Scrape_pages(keyword)
        db['web3'][keyword] = jobs
    return render_template('result_web3career.html', keyword=keyword, jobs=jobs)

@app.route("/static/wework/<keyword>")
def static_wework_result(keyword):
    keyword = (keyword or "").strip()
    if not keyword:
        return redirect("/search_weworkremotely")
    if keyword in db['wework']:
        jobs = db['wework'][keyword]
    else:
        jobs = rmscraper.rm_Scrape(keyword)
        db['wework'][keyword] = jobs
    return render_template('result_weworkremotely.html', keyword=keyword, jobs=jobs)


if __name__ == "__main__":
    app.run(debug=True)