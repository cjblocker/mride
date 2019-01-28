#! /usr/local/bin/python3
import requests
from datetime import datetime as dt 
from datetime import timedelta
import argparse
import os

__VERSION__ = '0.1'

BUS_API_ENDPOINT='http://www.theride.org/DesktopModules/AATA.EndPoint/Proxy.ashx?method=getpredictionsfromxml&stpid={}'

WORK_STOP_ID = 1550
HOME_STOP_ID = 1781
PIERPONT_STOP_ID = 0

def mac_pop_up(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

def setup_notify(stop_id, route_id, minutes):
    pass

def display_stop_info(stop_id, route_id='sort'):
    # print(requests.get(BUS_API_ENDPOINT.format(stop_id)).json())
    stop_loc = requests.get(BUS_API_ENDPOINT.format(stop_id)).json()['bustime-response']['prd']
    if not isinstance(stop_loc, list): stop_loc = [stop_loc]
    if route_id == 'sort':
        stop_loc.sort(key=lambda x: x['rt'])
    elif route_id == '*':
        pass
    else:
        stop_loc = [x for x in stop_loc if int(x['rt']) == int(route_id)]

    try:
        for bus in stop_loc:
            print("{:<25} {:>10}min  {:%I:%M %p}".format(bus['des'].strip(),bus['prdctdn'], dt.now()+timedelta(minutes=int(bus['prdctdn']))))
    except ValueError:
        print(stop_loc)

def parse_arguments():

    parser = argparse.ArgumentParser(description='CL application for checking Ann Arbor Public Bus')
    parser.add_argument('-V','--version', action="version", version=__VERSION__)

    stop_group = parser.add_mutually_exclusive_group()
    stop_group.add_argument('-H','--home', action="store_true",
                        help='Access Tuebingen & Lancashire Stop information')
    stop_group.add_argument('-w','--work', action="store_true",
                        help='Access Beal & Hayward Stop information. Default if no stop option given.')
    stop_group.add_argument('-p','--pierpont', action="store_true",
                        help='Access Pierpont Commons Stop information')
    stop_group.add_argument('-i','--id', type=int, nargs=1, metavar='stop_id',
                        help='Access the information for the stop with given id')

    parser.add_argument('-n','--notify', type=int, nargs='?', const=6, default=0, metavar='t',
                        help='Notify when the bus is t minutes away. Default t=6')
    parser.add_argument('-d','--display', action="store_true",
                        help='Display Stop information. Default if --notify option not specified')
    parser.add_argument('-r','--route', type=str, default='22', metavar='route_id',
                        help='The route number to return information on. Default = 22')


    args = parser.parse_args()
    stop_id = WORK_STOP_ID # Default
    if args.home:
        stop_id = HOME_STOP_ID
    elif args.work:
        stop_id = WORK_STOP_ID
    elif args.pierpont:
        stop_id = PIERPONT_STOP_ID
    elif args.id:
        stop_id = args.id

    if not args.notify:
        args.display = True # Default

    return stop_id, args.route, args.display, args.notify    

def main(stop_id=WORK_STOP_ID, route_id=22, do_print=True, notify_minutes=0):
    if do_print:
        display_stop_info(stop_id, route_id)
    if notify_minutes:
        setup_notify(stop_id, route_id, notify_minutes)

if __name__ == '__main__':
    # print("Now: {:%I:%M %p}".format(dt.now()))
    # print('Home:')
    # display_stop_info(1781)
    # print('Work:')
    # display_stop_info(1550)

    main(*parse_arguments())
