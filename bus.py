#! /usr/local/bin/python3
import requests
from datetime import datetime as dt 
from datetime import timedelta
import time
import argparse
import os
import functools

__VERSION__ = '0.1'

BUS_API_ENDPOINT='http://www.theride.org/DesktopModules/AATA.EndPoint/Proxy.ashx?method=getpredictionsfromxml&stpid={}'
UMICH_BUS_API_ENDPOINT='http://mbus.doublemap.com/map/v2/eta?stop={}' #['etas']['stopID']['etas']
UMICH_BUS_API_BUS_LIST='http://mbus.doublemap.com/map/v2/routes?id={}' # list all bus routes with name, id, stops, active
UMICH_BUS_API_STOP_LIST='http://mbus.doublemap.com/map/v2/stops?id={}' # get a stop name/code from id


WORK_STOP_ID = 1550
HOME_STOP_ID = 1781
PIERPONT_STOP_ID = 1714

# UMich Buses via Magic Bus
BURSLEY_BAITS = 1032
COMMUTER_NORTH = 1051
COMMUTER_SOUTH = 1049
NORTHWOOD = 1055

# UMich Stop IDs
N551_ID =  101 # BB Outbound from pierpont
N553_ID = 98   # Outside pierpont
C250_ID = 137 # CC little chem side
C251_ID = 138 # CC little museum side

def mac_pop_up(title, text):
    os.system("""osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

@functools.lru_cache()
def get_umich_route_name_from_id(route_id):
    try:
        route_info = requests.get(UMICH_BUS_API_BUS_LIST.format(route_id)).json()
        return route_info['name'], route_info['short_name']
    except KeyError:
        raise ValueError('No bus with route_id = {}'.format(route_id))

def get_umich_bus_stop_info(stop_id):
    try:
        stop_loc = requests.get(UMICH_BUS_API_ENDPOINT.format(stop_id)).json()['etas'][str(stop_id)]['etas']
    except KeyError:
        print('Currently No Buses for that Stop')

    if not isinstance(stop_loc, list): stop_loc = [stop_loc]

    stop_info = []
    for bus in stop_loc:
        name, short_name = get_umich_route_name_from_id(bus['route'])
        stop_info.append({
            'name': name,
            'short_name': short_name, 
            'route': bus['route'],
            'eta': bus['avg'],
            })
    # print(stop_info)
    return stop_info 

def get_mride_bus_stop_info(stop_id):
    # print(requests.get(BUS_API_ENDPOINT.format(stop_id)).json())
    try:
        stop_loc = requests.get(BUS_API_ENDPOINT.format(stop_id)).json()['bustime-response']['prd']
    except KeyError:
        print('Currently No Buses for that Stop')
        return

    if not isinstance(stop_loc, list): stop_loc = [stop_loc]

    stop_info = []
    for bus in stop_loc:
        stop_info.append({
            'name': bus['des'],
            'short_name': bus['rt'],
            'route': bus['rt'],
            'eta': bus['prdctdn'],
            })
    return stop_info 

def is_mride_id(stop_id):
    return stop_id > 999

def _get_stop_info(stop_id, route_id='*'):
    if is_mride_id(stop_id):
        stop_info = get_mride_bus_stop_info(stop_id)
    else:
        stop_info = get_umich_bus_stop_info(stop_id)

    if route_id == 'sort':
        stop_info.sort(key=lambda x: x['short_name'])
    elif route_id == '*':
        pass
    else: #isinstance(route_id, int)
        stop_info = [x for x in stop_info if str(x['short_name']) == str(route_id)]
    return stop_info


def setup_notify(stop_id, route_id, minutes):
    stop_loc = _get_stop_info(stop_id, route_id)
    time_left = min([int(bus['eta']) for bus in stop_loc])
    print(f"time_left = {time_left}")
    while time_left > minutes:
        time.sleep(60*(time_left - minutes)/2) # wait half expected amount
        stop_loc = _get_stop_info(stop_id, route_id)
        time_left = min([int(bus['eta']) for bus in stop_loc])
        print(f"time_left = {time_left}")
    mac_pop_up("Bus Stop", "Time to go, bus will be here in {} minutes".format(time_left))

def display_stop_info(stop_id, route_id='sort'):
    stop_loc = _get_stop_info(stop_id, route_id)

    try:
        for bus in stop_loc:
            print("{:<25} {:>10}min  {:%I:%M %p}".format(bus['name'].strip(),bus['eta'], dt.now()+timedelta(minutes=int(bus['eta']))))
    except ValueError:
        print(stop_loc)

def install():
    pass

def parse_arguments():

    parser = argparse.ArgumentParser(description='CL application for checking Ann Arbor Public Bus and UMich Bus info')
    parser.add_argument('-V','--version', action="version", version=__VERSION__)

    stop_group = parser.add_mutually_exclusive_group()
    stop_group.add_argument('-H','--home', action="store_true",
                        help='Access Tuebingen & Lancashire Stop information')
    stop_group.add_argument('-w','--work', action="store_true",
                        help='Access Beal & Hayward Stop information. Default if no stop option given.')
    stop_group.add_argument('-p','--pierpont', action="store_true",
                        help='Access Pierpont Commons Stop information')
    stop_group.add_argument('-i','--id', type=int, metavar='stop_id',
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

def run():
    main(*parse_arguments())

if __name__ == '__main__':
    run()
