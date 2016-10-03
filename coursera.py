import requests
from lxml import etree


def get_site_data(url):
    site_data = requests.get(url)
    return site_data.content


def get_courses_list(data):
    notes = etree.fromstring(data)

    for field in notes.findall('.//url'):
        print('Note to:',field.text)

def get_course_info(course_slug):
    pass


def output_courses_info_to_xlsx(filepath):
    pass


if __name__ == '__main__':
    pass
    url = 'https://www.coursera.org/sitemap~www~courses.xml'
    site_data = get_site_data(url)
    courses_list = get_courses_list(site_data)
    