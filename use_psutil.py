import psutil

print(psutil.cpu_count())
print(psutil.cpu_count(logical=False))
print(psutil.cpu_times())

for x in range(10):
    print(psutil.cpu_percent(interval=1, percpu=True))

print(psutil.virtual_memory())

print(psutil.disk_partitions())

print(psutil.disk_usage('c:'))

print(psutil.disk_io_counters())

print(psutil.net_io_counters())

print(psutil.net_if_addrs())

print(psutil.net_if_stats())

print(psutil.net_connections())
print(psutil.pids())

p = psutil.Process(14000)
print(p.name)
print(p.exe())
print(p.cmdline())
print(p.ppid())
print(p.parent())

print(p.children())
print(p.status())
print(p.username())
print(p.create_time())
#print(p.terminal())
print(p.cpu_times())
print(p.memory_info())
print(p.open_files())
print(p.connections())
print(p.num_threads())
print(p.threads())
print(p.environ())
print(p.terminate())
print(p.test())