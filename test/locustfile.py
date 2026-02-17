import libvirt
import time

from locust import FastHttpUser, task, between, events
from xml.etree import ElementTree

def log_vm_stat(csv_write_header):
    conn = libvirt.open("qemu:///system")
    if not conn:
        raise SystemExit("Failed to open connection to qemu:///system")

    dom = conn.lookupByName("load_test_default")
    if not dom:
        raise SystemExit("Failed to find domain")

    ts = time.time()

    print("Domain Block Device Performance")
    (rd_req, rd_bytes,
     wr_req, wr_bytes,
     err) = dom.blockStats("/var/lib/libvirt/images/load_test_default.img")

    print("Read requests issued: {} | "
          "Bytes read: {} | "
          "Write requests issued: {} | "
          "Bytes written: {} | "
          "Number of errors: {} | \n".format(
        rd_req, rd_bytes, wr_req, wr_bytes, err))
    if csv_write_header:
        with open("stats/domain_block_device_performance.csv", "w", encoding = "utf-8") as f:
            f.write("Timestamp,Read requests issued,Bytes read,"
                    "Write requests issued,Bytes written,Number of errors\n")

    with open("stats/domain_block_device_performance.csv", "a", encoding = "utf-8") as f:
        f.write("{},{},{},{},{},"
                "{}\n".format(int(ts), rd_req, rd_bytes, wr_req, wr_bytes, err))

    print("vCPU Performance")
    stats = dom.getCPUStats(True)
    print("CPU time: {cpu_time} | "
          "System time: {system_time} | "
          "User time: {user_time} | \n".format(**stats[0]))
    if csv_write_header:
        with open("stats/cpu_performance.csv", "w", encoding = "utf-8") as f:
            f.write("Timestamp,CPU time,System time,User time\n")

    with open("stats/cpu_performance.csv", "a", encoding = "utf-8") as f:
        f.write("{},{cpu_time},{system_time},"
                "{user_time}\n".format(int(ts), **stats[0]))

    print("Memory Statistics")
    stats = dom.memoryStats()
    print("Actual: {actual} | "
          "Swap in: {swap_in} | "
          "Swap out: {swap_out} | "
          "Major fault: {major_fault} | "
          "Minor fault: {minor_fault} | "
          "Unused: {unused} | "
          "Available: {available} | "
          "Usable: {usable} | "
          "Last update: {last_update} | "
          "Disk caches: {disk_caches} | "
          "Hugetlb pgalloc: {hugetlb_pgalloc} | "
          "Hugetlb pgfail: {hugetlb_pgfail} | "
          "RSS: {rss} | \n".format(**stats))
    if csv_write_header:
        with open("stats/memory_statistics.csv", "w", encoding = "utf-8") as f:
            f.write("Timestamp,Actual,Swap in,Swap out,Major fault,"
                    "Minor fault,Unused,Available,Usable,Last update,"
                    "Disk caches,Hugetlb pgalloc,Hugetlb pgfail,RSS\n")

    with open("stats/memory_statistics.csv", "a", encoding = "utf-8") as f:
        f.write("{},{actual},{swap_in},{swap_out},{major_fault},"
                "{minor_fault},{unused},{available},{usable},"
                "{last_update},{disk_caches},{hugetlb_pgalloc},"
                "{hugetlb_pgfail},{rss}\n".format(int(ts), **stats))

    print("I/O Statistics")
    tree = ElementTree.fromstring(dom.XMLDesc())
    iface = tree.find("devices/interface/target").get("dev")
    stats = dom.interfaceStats(iface)
    print("Read bytes: {} | "
          "Read packets: {} | "
          "Read errors: {} | "
          "Read drops: {} | "
          "Write bytes: {} | "
          "Write packets: {} | "
          "Write errors: {} | "
          "Write drops: {} | \n".format(*stats))
    if csv_write_header:
        with open("stats/io_statistics.csv", "w", encoding = "utf-8") as f:
            f.write("Timestamp,Read bytes,Read packets,Read errors,Read drops,"
                    "Write bytes,Write packets,Write errors,Write drops\n")

    with open("stats/io_statistics.csv", "a", encoding = "utf-8") as f:
        f.write("{},{},{},{},{},{},{},{},{}\n".format(int(ts), *stats))

    conn.close()

class LoadTestUser(FastHttpUser):
    wait_time = between(1, 5)

    @task
    def view_base(self):
        self.client.get("/")

    @task(3)
    def view_books(self):
        self.client.get("/books")

    @task(3)
    def view_book(self):
        self.client.get("/books/64f87e8c-3ecd-4411-978d-8f6381fa1c58")

    @task(2)
    def create_book(self):
        self.client.post("/books", json={"title": "Test Book", "author": "Test Elek"})

    @task(1)
    def update_book(self):
        self.client.put("/books/64f87e8c-3ecd-4411-978d-8f6381fa1c58", json={"pages": 999})

    @events.test_start.add_listener
    def on_test_start(**kwargs):
        print("============== On Test Start ==============\n")
        log_vm_stat(True)
        print("===========================================\n")

    @events.request.add_listener
    def on_request(**kwargs):
        ts = time.time()
        if int(ts) % 5 == 0:
            print("============== On Request ==============\n")
            log_vm_stat(False)
            print("========================================\n")

    @events.test_stop.add_listener
    def on_test_stop(**kwargs):
        print("============== On Test Stop ==============\n")
        log_vm_stat(False)
        print("==========================================\n")
