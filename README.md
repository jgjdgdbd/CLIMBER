# CLIMBER: Defending Phase Change Memory AgainstFlipping Address Attack


&#160; &#160; &#160; &#160; CLIMBER is a defense mechanism to neutralizeFlipping Address Attack.CLIMBER dynamically change harmful address mappings so that intensive writes to weak cells are redirected to strongcells.CLIMBER also conceals weak NVM cells from attackers by randomly mapping cold addresses to weak NVM regions.

CLIMBER Dependencies, Running, and Result
------------
**1.External Dependencies**  
&#160; &#160; &#160; &#160; Before running CLIMBER codes, it's essential that you have already install dependencies listing below.
* numpy
* python(>=2.7)
* Zsim-NVMain (We use Zsim to collect memory access trace. You can also use other simulators to collect trace) [axle-zsim-nvmain](https://github.com/AXLEproject/axle-zsim-nvmain)

**2.Running**

* First, get trace files by:
```javascript
[root @node1 CLIMBER/trace]# cat trace.tar.gz.* > trace.tar.gz
[root @node1 CLIMBER/trace]# tar -zxvf trace.tar.gz
```
* Then, copy the python files(.py) to the trace directory(CLIMBER/trace/\*/).
* Run CLIMBER codes by:
```javascript
[root @node1 CLIMBER/trace/*/]# python typeX_*_climber.py arg1 arg2
```
* X = 0 is non-attack; X = 1 is Inconsistent Write Attack.
* Arg1 and arg2 are used to enable our climber and WPRM schemes.

**3.Result**  
&#160; &#160; &#160; &#160; The endurance result are recorded by \*mm_climber.py in \*.dat files.


