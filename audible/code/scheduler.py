
# python imports
import schedule, time, datetime

# local imports
from audible import main


def scheduler():
    main()
    tm = str(datetime.datetime.now()).split(':')
    tim = 'Last Updated = ' + tm[0] + ':' + tm[1]
    print( '\n---------------------------------------------------\n', tim, '\n---------------------------------------------------\n')

schedule.every(1).hour.do(scheduler)
while True:
    schedule.run_pending()
    time.sleep(1)