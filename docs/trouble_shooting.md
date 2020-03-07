## docker0: iptables: No chain/target/match by that name

### Symptoms:
1. Interviews that call functions that access resources on the internet fail.
1. User gets an NGENIX timeout error.
1. After connecting to docker container, e.g.  ```docker exec -t -i *container_name* /bin/bash```, try ```nslookup www.google.com```. Fails to resolve DNS

### Solution

```
docker stop *container_name*
sudo iptables -t filer -F
sudo iptables -t filer -X
sudo systemctl restart docker
docker start *container_name*
```

### Cause
May be caused by changes to the firewall (enabling, disabling, reconfiguring) on the host computer.