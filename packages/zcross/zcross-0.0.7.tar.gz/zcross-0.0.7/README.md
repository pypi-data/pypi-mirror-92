# ZCross

ZCross is a python library used to read low pressure gas sections from various sources like [LXCat](https://lxcat.net/home/).

## Installation

To install this package just use pip:
``` shell
pip install zcross
```

Cross section databases are not provided by `ZCross`: however, it is possible to download the cross section tables of interest from [LXCat](https:://www.lxcat.net).
Once you download the cross sections in `XML` format, you can convert it into a format readable by `ZCross` using this [online converter](http://zcross.web.cern.ch/converter/).
It is now possible to save the cross section tables in any location (we suggest under `/opt/zcross_data`) and to define an enviroment variable pointing to that path:
``` bash
export ZCROSS_DATA=/opt/zcross_data
```
(you can add it to your `.profile` file)

## Examples

List the database availables:
``` python
from zcross import ZCross

z = ZCross()
for database in z.databases:
	print(database)
```
		
Show the groups and references of a speficic database:
``` python
from zcross import ZCross

z = ZCross()
database = z.databases[0]

for group in database.groups:
	print(group)

for reference in database.references:
	print(reference.bibtex())
```
		
Show the process of a specific group:
``` python
from zcross import ZCross

z = ZCross()
database = z.databases[0]
group      = database.groups[0]

for process in group.processes:
	print("Process {} (type: {}) : {}".format(process.id, process.collisionType, process))
	print("Comment: {}\n".format(process.comment))
```
	
Show the cross section table of a specific process:
``` python
from zcross import ZCross

z = ZCross()
database = z.databases[0]
group    = database.groups[0]
process  = group.processes[0]

print('Energy [{}],\tArea [{}]'.format(process.energy_units, process.cross_section_units))

for energy, area in zip(process.energy, process.cross_section):
	print('{:8.2f}\t{:e}'.format(energy, area))
```