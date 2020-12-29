import re
from datetime import datetime, timedelta,timezone

now = datetime.now()
print(now)
print(type(now))

dt = datetime(2015, 4, 19, 12, 20)
print(dt)

print(dt.timestamp())
t = 1429417200.0
print(datetime.fromtimestamp(t))
print(datetime.utcfromtimestamp(t))

cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
print(cday)
print(now.strftime('%a, %b %d %H:%M'))

print(now + timedelta(hours=10))
print(now - timedelta(days=1))
print(now + timedelta(days=2, hours=12))

tz_utc_8 = timezone(timedelta(hours=8))
dt = now.replace(tzinfo=tz_utc_8)
print(dt)
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
print(utc_dt)
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
print(bj_dt)
tokyo_d = utc_dt.astimezone(timezone(timedelta(hours=9)))
print(tokyo_d)
tokyo_d2 = bj_dt.astimezone(timezone(timedelta(hours=9)))
print(tokyo_d2)

def to_timestamp(dt_str, tz_str):
    dt = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
    zone = re.match(r'UTC([+-]\d+):(\d{2})',tz_str)
    tz_utc = timezone(timedelta(hours=int(zone.group(1))))
    tz_dt = dt.replace(tzinfo=tz_utc)
    return tz_dt.timestamp()
t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')

assert t1 == 1433121030.0, t1

t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
assert t2 == 1433121030.0, t2

print('ok')