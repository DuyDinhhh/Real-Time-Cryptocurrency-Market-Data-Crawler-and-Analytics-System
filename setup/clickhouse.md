# **Setup Clickhouse**

## **Download clickhouse in Docker:**

`docker run -d --name my-clickhouse-server -p 8123:8123 --ulimit nofile=262144:262144 clickhouse/clickhouse-server`

### **Start clickhouse**

`docker start my-clickhouse-server`


## **Login in DBeaver DB:**

```
Host: localhost
Port: 8123
User: default
Password: 
```

```
- Create table to storage data
CREATE TABLE trending_coin (
    rank UInt32,
    name String,
    symbol String,
    price Float64,
    _24h_percent Float64,
    _7d_percent Float64,
    _30d_percent Float64,
    marketcap UInt64,
    volume24h UInt64,
    updated_at DateTime
) ENGINE = MergeTree()
ORDER BY (updated_at);
```
 
