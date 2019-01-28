# Bus Stop CL Query

Queries Ann Arbor's Public bus service (theride.org) for bus information because their website is slow.

This is specifically designed to make accessing my most frequent stops easy, but could easily be adapted.

# Usage

```bash
$ bus_stop --help
usage: bus_stop [-h] [-V] [-H | -w | -p | -i stop_id] [-n [t]] [-d]
                [-r route_id]

CL application for checking Ann Arbor Public Bus

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -H, --home            Access Tuebingen & Lancashire Stop information
  -w, --work            Access Beal & Hayward Stop information. Default if no
                        stop option given.
  -p, --pierpont        Access Pierpont Commons Stop information
  -i stop_id, --id stop_id
                        Access the information for the stop with given id
  -n [t], --notify [t]  Notify when the bus is t minutes away. Default t=6
  -d, --display         Display Stop information. Default if --notify option
                        not specified
  -r route_id, --route route_id
                        The route number to return information on. Default = 22
```

# Future Work

- Add UMich Bus Services
- Finish Notify option

