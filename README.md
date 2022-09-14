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


## 2. Buffer Size and Buffer Hit/Miss

## Reference
<ul>
  <li>tpcc-mysql: Quick Start Guide, Github Repository, https://github.com/meeeejin/SWE3033-F2021/blob/main/week-1/reference/tpcc-mysql-install-guide.md</li>
  <li>Percona Lab : tpcc-mysql, Github repository, https://github.com/Percona-Lab/tpcc-mysql</li>
  <li>SWE3033_41, Sungkyunkwan University, Colleg of Computing</li>
</ul>

<li></li>
<i></i>
<b></b>
