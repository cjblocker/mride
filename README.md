# MRide CL Interface

Queries Ann Arbor's Public bus service (theride.org) for bus information because their website is slow.  
In addition to the Ann Arbor Public Bus, the tool also supports looking up UMich buses now via doublemap.  

This is specifically designed to make accessing my most frequent stops easy, but could easily be adapted.

## Install

```bash
pip install https://github.com/cjblocker/mride
```

## Usage

```bash
$ mride --help
usage: mride [-h] [-V] [-H | -w | -p | -i stop_id] [-n [t]] [-d] [-t]
             [-r route_id]

CL application for checking Ann Arbor Public Bus and UMich Bus info

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -H, --home            Access Tuebingen & Lancashire Stop information
  -w, --work            Access Beal & Hayward Stop information. Default if no
                        stop option given.
  -p, --pierpont        Access Pierpont Commons Public Stop information
  -i stop_id, --id stop_id
                        Access the information for the stop with given id.
                        Note 98 & 101 are both UMich stops near Pierpont, and
                        137 & 138 are CC Little stops.
  -n [t], --notify [t]  Notify when the bus is t minutes away. Default t=6
  -d, --display         Display Stop information. Default if --notify option
                        not specified. If --notify option present, this will
                        make it verbose.
  -t, --ticker          Display Stop information, updating every 30s. Cannot
                        be used with --notify or --display.
  -r route_id, --route route_id
                        The route number to return information on. Options
                        include BB for Bursely-Baits, 22, 65, CN for Commuter
                        North, etc. Default = *
```

## Future Work

- Multiple stops at once
- flag configuration file
- Easier access to UMich information
- UMich stop number lookup by name/code
- terminal colors? i.e. red for soon, or by route?
- Pop-Up or other notifications for not Mac computers

