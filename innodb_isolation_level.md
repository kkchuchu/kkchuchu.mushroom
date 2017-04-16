## MySQL InnoDB

### ACID

ATOMICITY:不可部分完成
CONSISTENCY:一致性
ISOLATION:隔離性
DURABILITY:耐久性

### Transaction Isolation Level

#### REPEATABLE LEVEL(Default)

- Non blocking read

Consistent reads within the same transaction read the snapshot established by the first read. 

This means that if you issue several plain (nonlocking) SELECT statements within the same transaction, these SELECT statements are consistent also with respect to each other.

- Blocking read (with_for_update or lock_in_share_mode)

#### READ COMMITTED

Each consistent read, even within the same transaction, sets and reads its own fresh snapshot.

So if a commit (by another transaction) between in two selects, the two selects result in different results.

#### READ UNCOMMITEED

SELECT statements are performed in a nonlocking fashion, but a possible earlier version of a row might be used. 

Thus, using this isolation level, such reads are not consistent. This is also called a dirty read.

#### SERIALIABLE

### Phantom Row

The so-called phantom problem occurs within a transaction when the same query produces different sets of rows at different times. 

For example, if a SELECT is executed twice, but returns a row the second time that was not returned the first time, the row is a “phantom” row.

### Reference
- [Official Document about isolation level](https://dev.mysql.com/doc/refman/5.7/en/innodb-transaction-isolation-levels.html)
