# MRide CL Interface

Queries Ann Arbor's Public bus service (theride.org) for bus information because their website is slow.  
In addition to the Ann Arbor Public Bus, the tool also supports looking up UMich buses now via doublemap.  

This is specifically designed to make accessing my most frequent stops easy, but could easily be adapted.

## Install

Requires Python 3

```bash
pip install git+https://github.com/cjblocker/mride.git
```

## Examples

Use `-d` to display stop information. (Also the default).
```bash
$ mride -d
22 | Pontiac - Dhu Varren to PPC    | 18 min | 01:48 PM
66 | Carpenter - Huron Pkwy to Meij | 23 min | 01:53 PM
22 | Pontiac - Dhu Varren to PPC    | 44 min | 02:14 PM
66 | Carpenter - Huron Pkwy to Meij | 53 min | 02:23 PM
```

Use the `-r` command to pick a route or set to `sort` to sort by route.
Use `-i` to pick a stop by ID. Default is Beal & Hayward Public Stop.
```bash
$ mride -r sort -i 98 #98 is outside pierpont
CS | Commuter South                 |  0 min | 01:31 PM
CS | Commuter South                 | 11 min | 01:42 PM
D2D| Diag to Diag to CCTC & Oxford  | 15 min | 01:46 PM
D2D| Diag to Diag to CCTC & Oxford  | 26 min | 01:57 PM
NW | Northwood                      |  3 min | 01:34 PM
NW | Northwood                      | 12 min | 01:43 PM
```

UMich routes are denoted by two letters
```bash
$ mride -r BB -i 101 #101 is across the street from pierpont, heading south
BB | Bursley-Baits                  |  6 min | 01:39 PM
BB | Bursley-Baits                  |  7 min | 01:40 PM
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

