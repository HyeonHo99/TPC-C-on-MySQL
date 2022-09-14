# TPC-C-on-MySQL
Analyis on MySQL DBMS with TPC-C Benchmark

## 1. TPC-C and Benchmarking
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

## 2. Run the TPC-C Benchmark
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
#### TpmC and Throughput
<ul>
  <li>Transactions per minute Count (TpmC) : 13683.75</li>
  <img src="/1/tpcc-run-results.png" width="400" heigh="300"></img>
  <li>Throughput changes over time (time interval: 10seconds)</li>
  <img src="" width="400" heigh="300"></img>
</ul>

#### Sysmtem Performance : Disk I/O
#### Sysmtem Performance : CPU Utility

## Reference
<ul>
  <li>tpcc-mysql: Quick Start Guide, Github Repository, https://github.com/meeeejin/SWE3033-F2021/blob/main/week-1/reference/tpcc-mysql-install-guide.md</li>
  <li>Percona Lab : tpcc-mysql, Github repository, https://github.com/Percona-Lab/tpcc-mysql</li>
  <li>SWE3033_41, Sungkyunkwan University, Colleg of Computing</li>
</ul>

<li></li>
<i></i>
<b></b>
