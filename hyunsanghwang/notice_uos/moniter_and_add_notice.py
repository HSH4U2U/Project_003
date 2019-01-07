import requests
from bs4 import BeautifulSoup
from .send_message import send_email, send_telegram
from .models import Notice
import ast
from accounts.models import Profile


# 올라온 공지 데이터 얻고 tag 분류하는 함수
def get_notice(sort_of_notice, page):
    url = sort_of_notice['view'] + str(page)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    title = soup.find('title').text.split('<')[0].strip()
    sort = soup.find('title').text.split('<')[1].strip()
    content = soup.findAll("li", {"id": "view_content"})[0].text
    # TODO: (tag 값 받아오는 거 해야함)tag 해당하는 것 있으면 tags 필드에 넣기
    all_tags = [
        '해외', '영어', '교환학생', '교환 학생', '창업', '대회', '상금',
        '시험', '전자전기컴퓨터', '전전컴', '인턴', '서울메이트', '서울 메이트'
        '버디'
        ]
    include_tags = []
    for tag in all_tags:
        if content:
            if title.count(tag) + sort.count(tag) + content.count(tag) > 0:
                include_tags.append(tag)
        elif title.count(tag) + sort.count(tag) > 0:
            include_tags.append(tag)

    # new_notice 에 해당 데이터 저장
    new_notice = {
        "seq": page,
        "sort_of_notice": sort_of_notice,
        "sort": sort,
        "title": title,
        "url": url,
        "tags": include_tags
    }
    return new_notice


# 얻은 new_notice 데이터를 모델에 저장하고, email 로 그 내용 보내기
def add_send_notice(new_notice):
    # Notice 모델에 새로운 object 로 저장
    notice = Notice(
        seq=new_notice["seq"],
        sort=new_notice["sort"],
        title=new_notice["title"],
        url=new_notice["url"],
        tags=str(new_notice["tags"])
    )
    notice.save()
    print("new save")

    title = new_notice["title"]
    message = new_notice["url"]
    tags = new_notice["tags"]
    # TODO: 여기에 해당 tag 가지고 있는 user 의 mail 주소 를 모델에서 가져오는 작업 수행
    receiver = []
    users = Profile.objects.all()
    for user in users:
        print(user.my_tags)
    # for tag in tags:
    #     for user in users:
    #         if tag in ast.literal_eval(user.my_tags) & user not in receiver:
    #             receiver.append(user)
    #             if user.email:
    #                 send_email(title, message, [user.email])
    #             if user.telegram_id:
    #                 send_telegram(title, message, user.telegram_id)
    # send_email(title, message, ['hsh700788@naver.com'])
    # send_telegram(title, message, "717570699")
    # print("send message")


# 공지 올라왔는 지 확인하고 올라왔으면 모델에 데이터 저장하는 함수
def monitor_and_add_send_notice(sort_of_notice, max_notice_seq):
    url = sort_of_notice['list']
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    a_tags = soup.findAll('a')
    seqs = []
    for a_tag in a_tags:
        a_tag_onclick = a_tag.get('onclick')
        if a_tag_onclick:
            if a_tag_onclick.find("fnView(") != -1:
                seq = a_tag_onclick.split("'")[3]
                seq = int(seq)
                seqs.append(seq)
    # 다음 공지 있나 확인하고, 공지 데이터 얻기 함수 실행
    new_notice_seq = max_notice_seq + 1
    if new_notice_seq in seqs:
        max_notice_seq = new_notice_seq
        new_notice = get_notice(sort_of_notice, max_notice_seq)
        add_send_notice(new_notice)
        monitor_and_add_send_notice(sort_of_notice, max_notice_seq)
    # 다음 공지가 지워졌을 수도 있으니 +4개까지 공지 확인
    else:
        i = 2
        while i < 5:
            certificate_seq = max_notice_seq + i
            if certificate_seq in seqs:
                max_notice_seq = certificate_seq
                new_notice = get_notice(sort_of_notice, max_notice_seq)
                add_send_notice(new_notice)
                monitor_and_add_send_notice(sort_of_notice, max_notice_seq)
                break
            i += 1
