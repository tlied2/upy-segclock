import utime as time
import ntptime

DOWMAP = [1, 2, 3, 4, 5, 6, 0]


def updatentp(ntp_host):
    ''' Wrapper around ntptime to set host per config (or fallback to pool.ntp.org)
        Also, generally ignores failures '''
    print(("Syncing RTC with NTP host: %s" % ntp_host))
    ntptime.host = ntp_host
    try:
        ntptime.settime()
    except OSError as tmpex:
        try:
            print(("Local NTP Host %s Failed, using pool.ntp.org" % ntp_host))
            ntptime.host = "pool.ntp.org"
            ntptime.settime()
        except OSError as tmpex:
            print(("Error setting time from NTP: %s" % tmpex))


def isDST(tmptime):
    ''' Ugly and technically wrong, US DST detection
        Rolls over at midnight - ie a couple hours before DST starts
        I actually like this, but would be happy to make it configurable if someone wants to fix '''
    year, month, day, hour, min, sec, dow, doy = time.localtime(tmptime)
    if month < 3 or month > 11:
        return False
    elif month > 3 and month < 11:
        return True
    prevSun = day - DOWMAP[dow]
    if month == 3:
        return prevSun >= 8
    else:
        return prevSun <= 0


def localize(offset=0, apply_dst=False):
    ''' Ugly timezone and DST offsetting '''
    tmptime = time.time()
    tmptime = tmptime + (offset * 60 * 60)
    if apply_dst and isDST(tmptime):
        tmptime = tmptime + (60 * 60)
    return time.localtime(tmptime)


def mktime():
    ''' Returns an ISO formatted string of UTC time for serial display '''
    year, month, day, hour, min, sec = localize()[:6]
    timestr = "{year}-{month:02d}-{day:02d}T{hour:02d}:{min:02d}:{sec:02d}"
    timestamp = timestr.format(
        year=year,
        month=month,
        day=day,
        hour=hour,
        min=min,
        sec=sec)
    return timestamp


def mkclock(config):
    ''' Returns a string with configurable formatting suitable for output for the display '''
    year, month, day, hour, min, sec = localize(config['offset'], apply_dst=True)[:6]

    if not config['24hour']:
        hour = hour % 12
        if hour < 1:
            hour = 12

    ts_format = "{hour:%sd}{colon}{min:02d}" % ('02' if config['pad'] else '')

    timestamp = ts_format.format(
        hour=hour,
        min=min,
        colon="" if sec % 2 else ":")

    print(timestamp)

    return timestamp


def print_time():
    ''' Print time to serial port '''
    timestamp = mktime()
    print(timestamp)


def clock():
    ''' Print time to serial port every second, forever '''
    while True:
        print_time()
        time.sleep(1)
