import pytest

from freezegun import freeze_time
from tests.utils import file_response
from city_scrapers.spiders.chi_transit import ChiTransitSpider
from datetime import date, time

freezer = freeze_time('2017-12-13 15:30:00')
freezer.start()

test_response = file_response('files/chi_transit.html')
spider = ChiTransitSpider()
parsed_items = [item for item in spider.parse(test_response) if isinstance(item, dict)]

freezer.stop()

def test_name():
    assert parsed_items[0]['name'] == 'Employee Retirement Review Committee Meeting'
    assert parsed_items[1]['name'] == 'Regular Board Meeting of Chicago Transit Board'
    assert parsed_items[2]['name'] == 'Committee on Strategic Planning & Service Delivery'


def test_description():
    assert parsed_items[0]['description'] == 'CTA Meetings -  Meeting Notice: http://www.transitchicago.com/assets/1/21/ADA_Advs_Commt_Mtg_Notice_for_April_9-2018.pdf?19085 Agenda: http://www.transitchicago.com/assets/1/21/ADA_Advs_Commt_Mtg_Agenda_for_4-9-2018.pdf?19504'
    assert parsed_items[1]['description'] == 'CTA Meetings -  Meeting Notice: http://www.transitchicago.com/assets/1/21/CANCELLATION_032218_ERR_Committee.pdf?19154'
    assert parsed_items[2]['description'] == 'Transit Board Meetings -  Meeting Notice: http://www.transitchicago.com/assets/1/21/Mar2018_-_Notice_-_Regular_Brd.pdf?19083 Agenda: http://www.transitchicago.com/assets/1/21/Mar2018_-_Regular_Board_Agenda.pdf?19084'


def test_start_time():
    assert parsed_items[0]['start_time'].isoformat() == '2017-12-13T15:30:00-05:00'
    
def test_start():
    EXPECTED_START = {
        'date': date(2018, 6, 15),
        'time': time(14, 0),
        'note': ''
    }
    assert parsed_items[0]['start_time'] == EXPECTED_START    


def test_start_time_after_mtg():
    assert parsed_items[1]['start_time'].isoformat() == '2017-12-13T18:30:00-05:00'


def test_classification():
    assert parsed_items[0]['classification'] == 'CTA Meetings'
    assert parsed_items[2]['classification'] == 'Transit Board Meetings'


# def test_id():
#    assert parsed_items[0]['id'] == 'chi_transit/201804091330/x/ada_advisory_committee_meeting'
#    assert parsed_items[2]['id'] == 'chi_transit/201803141130/x/regular_board_meeting_of_chicago_transit_board'


def test_status():
    assert parsed_items[0]['status'] == 'tentative'
    assert parsed_items[1]['status'] == 'cancelled'


@pytest.mark.parametrize('item', parsed_items)
def test_end_time(item):
    assert item['end_time'] is None


@pytest.mark.parametrize('item', parsed_items)
def test_all_day(item):
    assert item['all_day'] is False


@pytest.mark.parametrize('item', parsed_items)
def test_location(item):
    assert item['location'] == {
        'url': 'http://www.transitchicago.com',
        'name': 'Chicago Transit Authority 2nd Floor Boardroom',
        'address': '567 West Lake Street Chicago, IL',
        'coordinates': {
            'latitude': '41.88528',
            'longitude': '-87.64235',
        },
    }


@pytest.mark.parametrize('item', parsed_items)
def test__type(item):
    assert parsed_items[0]['_type'] == 'event'


@pytest.mark.parametrize('item', parsed_items)
def test_timezone(item):
    assert item['timezone'] == 'America/Chicago'
