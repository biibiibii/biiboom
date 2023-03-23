# biihub

## Hasura

### Migration

```
hasura init hasura --endpoint http://localhost:8090
```

create migration

```
hasura migrate create init --from-server --endpoint http://localhost:8090
```

apply migration to remote

```
hasura migrate apply --endpoint http://3.143.126.224:6060 --admin-secret "<admin-secret>"
```

``
