# TPC-C-on-MySQL
Analyis on MySQL DBMS with TPC-C Benchmark

## 0. TPC-C and Benchmarking
##### TPC
<ul>
  <li> TPC : Transaction Processing Performance Council</li>
  <li> TPC has become <b>de facto industry-standards</b> for enterprise benchmarks</li>
  <img src="https://www.tpc.org/tpc_common_library/images/tpc-header-image-logo-22.gif" width="500" height="100"></img>
</ul>

##### TPC-C
<ul>
  <li>Among many TPC series (TPC-E, TPC-H, TPC-VMS..), TPC-C will be used for benchmarking MySQL</li>
  <li>TPC-C is an <b>industry-standard OLTP benchmark</b> used to measure the performance of databases (OLTP: On-Line Transaction Processing)</li>
  <li>TPC-C simulates an <i>e-commerce</i> or <i>retail</i> company</li>
  <li>TPC-C assumes 5 types of well-defined transactions</li>
    <ol>
      <li>New-Order (Read/Write)</li>
      <li>Payment (Read/Write)</li>
      <li>Delivery (Read/Write)</li>
      <li>Order-Status (Read Only)</li>
      <li>Stock-Level (Read Only)</li>
     </ol>
  <li><b>Throughput of TPC-C (trx)</b>, whic refers to the number of New-Order transactions exectued per minute, is the most important performance measure</li>
  <li><b>TpmC</b> (Transactions per mintue Count) summarizes the Throughput very well</li>
  <li>Random I/O intensive workload : TPC-C performs 65% Read operations nad 35% write operations</li>
  <li>TPC-C Relationship Diagram</li>
  <img src="https://www.yugabyte.com/wp-content/uploads/2020/07/entity-relationship-diagram-for-the-TPC-C-workload-yugabytedb-performance-benchmarks.png" width="600" height="300"></img>
</ul>

## Installation
#### Prerequisites
<ul>
  <li>libreadline,libaio,libmysqlclient-dev</li>
  <li>build-essential, cmake, libncurses5, libncurses5-dev, bison</li>
  <li>MySQL5.7</li>
  
  ```consle
  $ wget https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-5.7.33.tar.gz
  ```
  <li>TPCC-mysql from Percona GitHub repository</li>
  
  ```consle
  $ git clone https://github.com/Percona-Lab/tpcc-mysql.git
  ```
  :+1: For detailed and friendly installation process, visit [tpcc-mysql: Quick Start Guide](https://github.com/meeeejin/SWE3033-F2021/blob/main/week-1/reference/tpcc-mysql-install-guide.md)
</ul>

## 1. Run the TPC-C Benchmark
While running the TPC-C benchmark on MySQL, analyze results, performance metrics and also monitor system performance
<ol>
  <li><b>Set buffer pool size</b> in my.cnf (mysql configuration file): Here we set, the buffer pool size as 10% of TPC-C database size, so 200M</li>
  
  ```consle
  $ vi /path/to/my.cnf
...
innodb_buffer_pool_size=200M
...
  ```
  
  <li><b>Start MySQL server</b></li>
  
  ```consle
  $ vi /path/to/my.cnf
$ ./bin/mysqld_safe --defaults-file=/path/to/my.cnf
  ```
  
  <li><b>Run TPC-C</b></li>
  
  ```consle
$ ./tpcc_start -h 127.0.0.1 -S /tmp/mysql.sock -d tpcc -u root -p "yourPassword" -w 20 -c 8 -r 10 -l 1200 | tee tpcc-result.txt  
  ```
</ol>

### Results
#### (1) TpmC and Throughput
<ul>
  <li>Transactions per minute Count (TpmC) : 13683.75</li>
  <img src="/1/tpcc-run-results.png" width="400" heigh="300"></img>
  <li>Throughput changes over time (time interval: 10seconds)</li>
  <img src="/1/trx_graph.png" width="450" heigh="450"></img><br>
  
   ```consle
  10, trx: 12920, 95%: 9.483, 99%: 18.738, max_rt: 213.169, 12919|98.778, 1292|101.096, 1293|443.955, 1293|670.842
  20, trx: 12666, 95%: 7.074, 99%: 15.578, max_rt: 53.733, 12668|50.420, 1267|35.846, 1266|58.292, 1267|37.421
  30, trx: 13269, 95%: 6.806, 99%: 13.126, max_rt: 41.425, 13267|27.968, 1327|32.242, 1327|40.529, 1327|29.580
  ```
  10 - indicates the seconds from the start of the benchmark <br>
  'trx' - indicates New Order transactinos executed during the given interval (in this case, for the previous 10 seconds)<br>
  '95%' - refers to the 95% Response time of New Order transactions per given interval <br>
  '99%' - refers to the 99% Response time of New Order transactions per given interval <br>
  'max_rt' - refers to the Maximum Response time of New Order transactions per given interval <br>
  rest columns can be ignored<br>
  <li>Response Time Change Visualization</li>
  <img src="/1/rt_graph.png" width="450" heigh="450"></img><br>
</ul>

#### (2) Sysmtem Performance : Disk I/O
Measured with iostat

```consle
  $ iostat -mx 1
```
Here we note two values : <b>%r/s, %w/s</b>
<ul>
  <li>%r/s : the number of read requests that were issued to the (read) device per second</li>
  <li>%w/s : the number of write requests that were issued to the (read) device per second</li>
</ul>
Average r/s was 7068 meanwhile average w/s was 3900. <br>
Thus, average raito of read/write (from/on Disk) was 64.43 : 35.56, which approximates 65:35 as expected<br>

#### (3) Sysmtem Performance : CPU Utility
Measured with mpstat

```consle
$ mpstat -P ALL 1
```
Here we note three values : <b>%usr, %sys, %idle</b>
<ul>
  <li>%usr : the percentage of CPU utilization that occurred while executing at the user level (application)</li>
  <li>%sys : the percentage of CPU utilization that occurred while executing at the system level (kernel)</li>
  <li>%idle : the percentage of time that the CPU or CPUs were idle and the system did not have an outstanding disk I/O request</li>
</ul>
Average %usr was 27.45, average %sys was 7.45 and average %idle was 42.16 while TPC-C benchmark run.


## 2. Measure MySQL Performance by Varying the Buffer Size
### Database I/O Architecture
<ol>
  Every database shares the below I/O architecture
  <li>SQL statements are translated into Logical Page Read/Write operations</li>
  <li>If requested page exists in database buffer(buffer pool), physical page read/write operations occur immediately <b>[Buffer Hit]</b></li>
  <li>If the page is not in in database buffer, it is pulled onto database buffer first, then the physical operations occur <b>[Buffer Miss]</b></li>
  In case of Buffer Miss, if there's no empty frame in buffer pool, a victim frame should be chosen, in our case, according to LRU policy. <br>
  If the victim frame is clean (not modified), it is simply discarded.<br>
  If the victim frame is dirty (modified/updated), it is written back into Disk storage first, then erased.<br>
  <img src="/2/db-architecture.png" width="300" heigh="400"></img><br>
</ol>

### Buffer Replacement Policy
<ul>
  <li>A victim buffer frame is chosen for replacement by a replacement policy</li>
  <li>Types of replacement policies : Random, FIFO, LRU, MRU, Clock,...</li>
  <li>Better replacement policy result in a higher buffer hit ratio and buffer hit ratio has a huge impact on DBMS performance time</li>
  <li>One Buffer miss usually makes one or two more disk I/O</li>
  <li>Disk access time = DRAM access time * 1000</li>
  <li>Buffer Hit Ratio = number of buffer hits / number of page requests to buffer cache</li>
  <li>Buffer Pool : area in main memory where InnoDB caches data as it is accessed</li>
</ul>

### Buffer Pool LRU Algorithm (codes in 'buf/buf0lru.cc')
- MySQL mangages the buffer pool with <b>two sub-lists using a variation of LRU</b>
- Mechanism
  <ol>
    <li>When a page is initially accessed to buffer pool, it is inserted at the midpoint</li>
    <li>
      <ul>Page Hits in the
          <li>Old sub-list: makes the page young (move the page to the head of the new sub-list)</li>
          <li>New sub-list: moves the page to the head of the new sub-list only if they are a certain distance from the head</li>
      </ul>
    </li>
    <li>Least recently used pages are moved to the tail of the list and are evicted</li>
  </ol>
- Why keeps two sub-lists? => To be resistant to buffer pool scan (Large scans, Read-ahead)
- To minimize the amount of data that is brought into the buffer pool and never accessed again (they reside in old sub-list and eventually evicted quick)
- To make sure frequently accessed pages reamin in the buffer pool (they usually reside in new sub-list)<br>
<img src="/2/LRU-list.png" width="300" heigh="650"></img><br>

### Measure Buffer Hit/Miss Ratio on different Buffer Pool Sizes
- Buffer pool size can be modified by changing values for "innodb_buffer_pool_size" in MySQL Configuration file (my.cnf)
- We set buffer pool size to 10%, 20%, 30%, 40%, 50% of TPC-C database size. (Respectively, 200MB, 400MB, 600MB, 800MB 1GB)
- Then conduct experiment (Run TPC-C benchmark)

<ol>
  <li>Before starting MySQL server, modify buffer pool size to 10%(then, 20%, 30%, 40%, 50%) of your TPC-C database size<br>
  Here we set database size as 2GB (= 20 warehouses)<br>
  In this case, change the value of 'innodb_buf_pool_size' in my.cnf (mysql configuration file) to 200M (200MB)</li><br>
  
  ```consle
  $ vi /path/to/my.cnf
...
innodb_buffer_pool_size=200M
...
  ```
  
  <li>Start MySQL server<br></li>
  
  ```consle
  $ ./bin/mysqld_safe --defaults-file=/path/to/my.cnf
  ```
  
  <li>Run the TPC-C benchmark<br></li>
  
  ```consle
  $ ./tpcc_start -h 127.0.0.1 -S /tmp/mysql.sock -d tpcc -u root -p "yourPassword" -w 20 -c 8 -r 10 -l 1200 | tee tpcc-result.txt
  ```
  
  <li>Keep track of buffer hit/miss ratio <br></li>
  Open MySQL terminal and use 'SHOW ENGINE INNODB STATUS' command
  
  
  ```consle
  $ ./bin/mysql -uroot -pyourPassword
  Welcome to the MySQL monitor.  Commands end with ; or \g.Your MySQL connection id is 8Server version: 8.0.15 Source distribution
Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> show engine innodb status;
...
----------------------
BUFFER POOL AND MEMORY
----------------------
Total large memory allocated 2353004544
Dictionary memory allocated 373557
Buffer pool size   524288
Free buffers       0
Database pages     524287
Old database pages 193695
Modified db pages  0
Pending reads      1
Pending writes: LRU 0, flush list 0, single page 0
Pages made young 0, not young 36985
0.00 youngs/s, 2465.50 non-youngs/s
Pages read 576950, created 160, written 177
38431.37 reads/s, 0.13 creates/s, 11.13 writes/s
Buffer pool hit rate 986 / 1000, young-making rate 0 / 1000 not 63 / 1000
Pages read ahead 0.00/s, evicted without access 3444.10/s, Random read ahead 0.00/s
LRU len: 524287, unzip_LRU len: 0
I/O sum[0]:cur[0], unzip sum[0]:cur[0]
...
  ```
  
</ol>

#### Results: Buffer Hit Ratio Comparison
- We measure 'buffer hit rate' with above command, two times: first in the beginning of the TPC-C run and in the end.
- Then, use average of two values as the respresentative hit ration.
- <b>Bigger buffer pool size resulted in higher the buffer hit ratio</b> (as expected)<br>
<img src="/2/buffer-hit-comparison.png" width="300" heigh="300"></img><br>

#### Results: TpmC and TPC-C Throughput Comparison
- <b> Again, bigger buffer pool size resulted in better TpmC and better throughput</b> <br>
<img src="/2/tpmc.png" width="350" heigh="350"></img>
<img src="/2/throughput-comparison.png" width="350" heigh="350"></img><br>

### Results: Disk Read / Disk Write Ration Comparison
- We leverage Disk I/O monitoring tool, 'iostat'

 ```consle
  $ timeout -k 1 1200 iostat -mx 1
  ```
  
- Above timeout command sends TERM signal after 1200 seconds to iostat command. If this doesn't terminate the iostat command, timeout sends KILL signal after 1 second. (KILL signal can't be blocked)
- We examine 'r/s' and 'w/s' column, which respectively means 'Disk Reads per Second' and 'Disk Writes per Second'.<br>
<img src="/2/read-write-comparison.png" width="350" heigh="350"></img><br>
- We note that as buffer size increases, <b>the number of both I/O decreases</b>. It can be implied that as the Main Memory (buffer cache) gets big enough to contain most pages, the need to visit Disk Storage decreases.
- We also note that with increasing buffer pool size, <b>ratio of writes to reads increases</b>. ISame interpretation from above can be implied
  

## Reference
<ul>
  <li>Percona Lab : tpcc-mysql, Github repository, https://github.com/Percona-Lab/tpcc-mysql</li>
  <li>tpcc-mysql: Quick Start Guide, Github Repository, https://github.com/meeeejin/SWE3033-F2021/blob/main/week-1/reference/tpcc-mysql-install-guide.md</li>
  <li>SWE3033_41, Sungkyunkwan University, College of Computing</li>
</ul>

<i></i>
<b></b>
