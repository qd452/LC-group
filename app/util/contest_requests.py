import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from collections import defaultdict, OrderedDict
import datetime
from bs4 import BeautifulSoup
from dataclasses import dataclass, field, asdict
from typing import List
from pprint import pprint


@dataclass
class Contest:
    contest_num: str
    start_time: str = ''
    participated_user_num: int = 0
    registered_user_num: int = 0
    questions: dict = field(default_factory=dict)
    user_ranks: List[dict] = field(default_factory=list)


def search_pagination(page, contest_num, users):
    r = requests.get(
        f'https://leetcode.com/contest/api/ranking/{contest_num}/?pagination={page}&region=global'
    ).json()
    total_rank = r['total_rank']
    submissions = r['submissions']
    page_user = []
    for i, rank in enumerate(total_rank):
        if rank['username'] in users:
            submission = submissions[i]
            page_user.append({'rank': rank, 'submissions': submission})
    return page_user


def get_user_info_parallel(users):
    max_workers = max(len(users), 50)
    user_info_dct = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_user = {
            executor.submit(get_user_info, user): user
            for user in users
        }
        for future in as_completed(future_to_user):
            user = future_to_user[future]
            try:
                user_info = future.result()
            except:
                user_info = [None, None]
            user_info_dct[user] = user_info
    return user_info_dct


def get_user_info(user):
    r = requests.get(f'https://leetcode.com/{user}/')
    soup = BeautifulSoup(r.content, 'html.parser')
    list_group_item = soup.findAll(class_='list-group-item')
    rating_obj = next(x for x in list_group_item if 'Rating' in x.text)
    solved_questions_obj = next(x for x in list_group_item
                                if 'Solved Question' in x.text)
    rating = rating_obj.find('span').text.strip()
    solved_questions = solved_questions_obj.find('span').text.strip().split(
        '/')[0].strip()
    return rating, solved_questions


def format_data(users, questions_dct, start_time, participated_user_num):
    df_dct = defaultdict(list)
    for u in users:
        rank = u['rank']['rank']
        username = u['rank']['username']
        df_dct['rank'].append(rank)
        df_dct['percentile'].append(f'{(rank/participated_user_num):.0%}')
        df_dct['username'].append(username)
        df_dct['score'].append(u['rank']['score'])
        took_seconds = u['rank']['finish_time'] - start_time
        finish_time = str(datetime.timedelta(seconds=took_seconds))
        df_dct['finish_time'].append(finish_time)
        for q_title, q_id in questions_dct.items():
            contents = None
            try:
                sec = u['submissions'][q_id]['date'] - start_time
                fail_count = u['submissions'][q_id]['fail_count']
                q_time = str(datetime.timedelta(seconds=sec))
                contents = f'{q_time}({fail_count})' if fail_count > 0 else str(
                    q_time)
            except:
                pass
            df_dct[q_title].append(contents)
        df_dct['pagination'].append(rank // 25 + 1)
        rating, solved_questions = get_user_info(username)
        df_dct['rating'].append(rating)
        df_dct['solved_questions'].append(solved_questions)
    df = pd.DataFrame(df_dct)
    df.sort_values(by=['rank'], inplace=True)
    return df


def get_contest(contest_num: str):
    r = requests.get(f'https://leetcode.com/contest/api/info/{contest_num}/')
    contest = r.json()
    title = contest['contest']['title']
    start_time = contest['contest']['start_time']
    questions = contest['questions']
    participated_user_num = contest['user_num']
    # print(title)
    # print(datetime.datetime.fromtimestamp(start_time))
    questions_dct = OrderedDict()
    for i, q in enumerate(questions, start=1):
        questions_dct[f'Q{i} [{q["credit"]}]'] = str(q['question_id'])
    # print(questions_dct)
    r = requests.get(
        f'https://leetcode.com/contest/api/ranking/{contest_num}/?pagination=2&region=global'
    )
    pagination = r.json()
    registered_user_num = pagination['user_num']

    return Contest(title, start_time, participated_user_num,
                   registered_user_num, questions_dct)


def get_user_ranking(contest_num: str, total_pages: str, users: set):
    user_ranks = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [
            executor.submit(lambda x: search_pagination(*x),
                            (page, contest_num, users))
            for page in range(1, total_pages + 1)
        ]
        for future in as_completed(futures):
            user_ranks.extend(future.result())
    return user_ranks

    # with open(f'{contest_num}.json', 'w') as f:
    #     json.dump(rslt, f, indent=4)


def get_contest_user_ranking(contest_num, users):
    cont_obj = get_contest(contest_num)
    total_pages = cont_obj.registered_user_num // 25
    user_ranks = get_user_ranking(contest_num, total_pages, users)
    cont_obj.user_ranks = user_ranks
    return cont_obj


def main(contest_num, users):
    cont_obj = get_contest_user_ranking(contest_num, users)
    df = format_data(cont_obj.user_ranks, cont_obj.questions,
                     cont_obj.start_time, cont_obj.participated_user_num)
    print(
        f'participated user num: {cont_obj.participated_user_num}, ' + \
        f'registered user num: {cont_obj.registered_user_num}'
    )
    pprint(cont_obj.user_ranks[0])
    print(df)
    df.to_csv(f'{contest_num}.csv')

if __name__ == '__main__':
    contest_num = 'weekly-contest-165'
    # contest_num = 'biweekly-contest-14'
    users = {
        'qd452', 'guoqiang2648', 'thread_start', 'liu_diansheng', 'sylyongli',
        'lijiang3800045', 'jessica_x_1028', 'lqianzhen', 'coffeebenzene',
        'gohuishan', 'M00nwell', 'pumbaa5', 'farmerboy'
    }
    # contest = get_contest(contest_num)
    # pprint(asdict(contest))
    main(contest_num, users)

    # get_user_info('qd452')
