from django.shortcuts import render
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from .moniter_and_add_notice import monitor_and_add_send_notice
from .models import Notice
from multiprocessing import Pool


common_notice = {
    'list': 'http://uos.ac.kr/korNotice/list.do?list_id=FA1',
    'view': 'http://uos.ac.kr/korNotice/view.do?list_id=FA1&seq=',
    'name': '일반공지'
}
bachelor_notice = {
    'list': 'http://uos.ac.kr/korNotice/list.do?list_id=FA2',
    'view': 'http://uos.ac.kr/korNotice/view.do?list_id=FA2&seq=',
    'name': '학사공지'
}
employment_notice = {
    'list': 'http://uos.ac.kr/korNotice/list.do?list_id=FA34',
    'view': 'http://uos.ac.kr/korNotice/view.do?list_id=FA34&seq=',
    'name': '직원채용'
}
notices = [common_notice, bachelor_notice, employment_notice]

# scheduler = BackgroundScheduler()
# scheduler.add_jobstore(DjangoJobStore(), "default")


# 10분마다 전체 함수 실행
# TODO: pool 로 각 공지 멀티 테스킹 처리
# @register_job(scheduler, "interval", seconds=10)
# def test_job():
#     def job(notice):
#         max_notice_seq = Notice.objects.filter(sort=notice["name"]).values("seq").last()["seq"]
#         monitor_and_add_send_notice(notice, max_notice_seq)
#     for notice in notices:
#         job(notice)
#
#
# register_events(scheduler)
#
# scheduler.start()
# print("Scheduler started!")

