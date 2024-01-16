# biihub

```
push main branch of git will deploy frontend to PROD env
PROD env is hosting on vercel.
```

## Contribution Guide

1. Pick or create an issue.
2. Submit your code to the `dev` branch.
3. Create a pull requests to `main` branch.

That's all; enjoy coding.

## [ui](./ui/README.md)

current frontend

## [etl](./etl/README.md)

data crawl and store

## [Hasura](https://github.com/hasura/graphql-engine)

API platform

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
