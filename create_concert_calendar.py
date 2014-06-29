import re, os
from datetime import datetime, timedelta
from icalendar import Calendar, Event, vText

class Concert():
  def __init__(self, band, concert_datetime, location):
    self.band = band
    self.concert_datetime = concert_datetime
    self.location = location

  def __str__(self):
    return "%s : %s : %s" % (self.band, self.concert_datetime, self.location)

  @classmethod
  def from_text_file(klass, concert_date, concert_info_string):
    concert_info = concert_info_string.split(". ")
    band = concert_info[0]
    concert_datetime = klass.__get_concert_datetime(concert_date, concert_info[1])
    location = concert_info[2]
    return klass(band, concert_datetime, location)

  @staticmethod
  def __get_concert_datetime(concert_date, concert_time_info):
    if re.match("\d{1,2}\w\w", concert_time_info):
      concert_time = datetime.strptime(concert_time_info + " EDT", "%I%p %Z").time()
    elif re.match("\d{1,2}:\d\d\w\w", concert_time_info):
      concert_time = datetime.strptime(concert_time_info + " EDT", "%I:%M%p %Z").time()
    return datetime.combine(concert_date, concert_time)
    else:
      raise Error('Unable to parse concert time')

class ConcertCalendar(Calendar):
  def __init__(self):
    super(Calendar, self).__init__()
    self.add('summary', 'NYC Summer 2014 Free Concerts')
    self.add('prodid', '-//NYC Summer 2014 Free Concerts//github.com/gpleiss')

  def add_concert(self, concert):
    event = Event()
    event.add('summary', "Concert: %s" % concert.band)
    event.add('dtstart', concert.concert_datetime)
    event.add('dtend', concert.concert_datetime + timedelta(hours=3))
    event.add('location', vText(concert.location))
    self.add_component(event)

  def save(self, filename='concert_calendar.ics'):
    with open(filename, 'wb') as f:
      f.write(cal.to_ical())

  def __str__(self):
    return cal.to_ical().replace('\r\n', '\n').strip()

class ConcertScraper():
  def scrape(self, filename="concerts.txt"):
    concerts = []

    all_text = ""
    with open("concerts.txt") as f:
      all_text = f.read()

    date_concerts_info_strings = all_text.split("\n\n")

    for date_concerts_info_string in date_concerts_info_strings:
      concert_date_info, concert_info_strings = self.__split_date_concerts_info(date_concerts_info_string)
      concert_date = self.__date_from_string(concert_date_info)

      for concert_info_string in concert_info_strings:
        concert = Concert.from_text_file(concert_date, concert_info_string)
        concerts.append(concert)

    return concerts

  def __split_date_concerts_info(self, date_concerts_info_string):
    split_info = date_concerts_info_string.split("\n")
    concert_date_info = split_info[0]
    concert_info_strings = split_info[1:]
    return concert_date_info, concert_info_strings

  def __strip_suffex_off_date_string(self, date_string):
    return re.match("\w+ \d+", date_string).group(0)

  def __date_from_string(self, date_string):
    processed_date_string = "2014 " + self.__strip_suffex_off_date_string(date_string)
    return datetime.strptime(processed_date_string , "%Y %B %d").date()


if __name__ == '__main__':
  cal = ConcertCalendar()
  [cal.add_concert(concert) for concert in ConcertScraper().scrape()]
  print cal
  cal.save()

