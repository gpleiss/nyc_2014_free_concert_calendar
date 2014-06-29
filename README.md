# NYC 2014 Free Concert Calendar

A python script that generates a calendar of free summer concerts in NYC.

The concert data is stored in the file "concerts.txt", and is originally from [The Village Voice](http://blogs.villagevoice.com/music/2014/05/the_ultimate_list_free_summer_concerts_nyc.php).

The calendar itself is stored in the file "concert_calendar.ics"

## Adding the calendar to Google Calendar

- Visit your Google Calendar
- Click the down arrow by "Other Calendars"
- Click "Add by URL"
- Paste in the following URL: "https://raw.githubusercontent.com/gpleiss/nyc_2014_free_concert_calendar/master/concert_calendar.ics?nocache" and click "Add Calendar"

## Generating the calendar via the script

### Setup

The script "create_concert_calendar.py" requires the following

- Python 2.7
- Python icalendar package ([installation information here](http://icalendar.readthedocs.org/en/latest/))

### Run

```
python create_concert_calendar.py
```
