from machine import RTC

rtc = RTC()
rtc.datetime((2021, 2, 13, 7, 21, 43, 0, 0)) # set date & time
rtc.datetime() # get date and time

print(rtc.datetime())