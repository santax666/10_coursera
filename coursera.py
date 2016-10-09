import requests
import random
import string
import argparse
import datetime
from openpyxl import Workbook
from bs4 import BeautifulSoup


def send_get_request(url):
    site_data = requests.get(url, allow_redirects=False)
    return site_data


def get_all_courses():
    courses_list = []
    url = ''.join(('https://api.coursera.org/api/courses.v1?fields=',
                  'primaryLanguages,subtitleLanguages,startDate,workload'))
    resp_json = send_get_request(url).json()
    courses_list = resp_json['elements'].copy()
    next_page = resp_json.get('paging', {}).get('next')
    while next_page is not None:
        resp_json = send_get_request(url+'&start={0}'.format(next_page)).json()
        courses_list.extend(resp_json['elements'].copy())
        next_page = resp_json.get('paging', {}).get('next')
    return courses_list


def get_list_random_numbers(max_number, quantity_courses=20):
    return random.sample(range(max_number), quantity_courses)


def convert_list_to_str(data):
    return ','.join(data)


def get_url_course(slug):
    course_type = ('learn', 'course',)
    for course in course_type:
        url = 'https://www.coursera.org/{0}/{1}'.format(course, slug)
        http_code = send_get_request(url).status_code
        headers = send_get_request(url).history
        if http_code == 200:
            break
    return url


def convert_posix_to_datetime(value):
    milliseconds_in_second = 1000
    value = int(value) / milliseconds_in_second
    return datetime.datetime.fromtimestamp(value).strftime('%d-%m-%Y')


def get_random_courses_info(data):
    courses_list = []
    courses_count = len(data)
    list_numbers = get_list_random_numbers(courses_count)
    for number in list_numbers:
        name = data[number].get('name')
        primary_languages = data[number].get('primaryLanguages')
        primary_languages = convert_list_to_str(primary_languages)
        subtitle_languages = data[number].get('subtitleLanguages')
        subtitle_languages = convert_list_to_str(subtitle_languages)
        start_date = data[number].get('startDate')
        if start_date is not None:
            start_date = convert_posix_to_datetime(start_date)
        work_load = data[number].get('workload')
        url = get_url_course(data[number].get('slug'))
        if url is not None:
            rating = get_rating_course(url)
        else:
            rating = None
        course_info = (name, primary_languages, subtitle_languages,
                       start_date, work_load, rating,)
        courses_list.append(course_info)
    return courses_list


def find_prefix(soup):
    class_param = 'rc-PhoenixCdpApplication'
    rid = soup.find('div', {'class': class_param})
    if rid is not None:
        return rid['data-reactid']


def find_rating_course(soup, prefix):
    param = prefix + '.0.0.1.1.0.0.0:$section_overview.1.6.0.0.6.1.0.2.0'
    rating = soup.find('span', {'data-reactid': param})
    if rating is not None:
        return rating.string


def get_rating_course(url):
    responce = send_get_request(url).content
    course_soup = BeautifulSoup(responce, "html.parser")
    reactid = find_prefix(course_soup)
    rating = find_rating_course(course_soup, reactid)
    return rating


def output_courses_info_to_xlsx(courses_list, filepath):
    work_book = Workbook()
    work_sheet = work_book.active

    sheet_title = ('Название курса', 'Основные языки', 'Дополнительные языки',
                   'Дата начала', ' Количество недель', 'Рейтинг')
    for title_count, title in enumerate(sheet_title, 1):
        work_sheet.cell(row=1, column=title_count).value = title
    for course_number, course in enumerate(courses_list, 2):
        for param_number, param in enumerate(course, 1):
            work_sheet.cell(row=course_number,
                            column=param_number).value = param
    work_book.save(filepath)


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', default='courses.xlsx',
                        help="XLSX-файл для сохранения")
    return parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args()
    xlsx_file = namespace.filepath

    courses_list = get_all_courses()
    courses_info = get_random_courses_info(courses_list)
    output_courses_info_to_xlsx(courses_info, xlsx_file)
