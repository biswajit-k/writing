`select` can be used in "core" and "orm" both.
it needs to be run by `session.execute()`

so ways in sqlalchemy are:

* **core** - tables, and dsl functions(select, filter_by, order_by, join)
* **orm model + dsl** - create `User` model + DSL using `select()` - return result as list. To insert, need to provide objects as a dict. Eg- `{name: "jon", "id": 43}`
* **only orm** - model + session.function(), objects as User(...)

---

orm model needs primary key as the identity map of session distinguish objects based on it.

---

session uses data structure identity map to store objects

---
[unit of work pattern](https://martinfowler.com/eaaCatalog/unitOfWork.html) - maintains state of database whatever changes are made are finally written together

---
`flush` vs `commit` : 

`flush` sends changes to database but it is not permanant yet, so it can be rolledback. When `commit` is made changes get permanant.

When we retrieve data from database in a session then, $$data = fetch(database) + flushed\ uncommitted\ changes\ in\ session$$

By default `autoFlush` is `true`, so each operation you do gets written to database, hence an **order** is maintained. However, if you set it to `false` then below example
    
    
    session.delete(usr)

    updated_user = User(...)
    session.add(updated_user)   # can be done 1st...ERR: as usr already exist

    session.commit()

Above happens because if changes are not flushed, any operation can get written first.

In all two advantages of flush:
    
1. Order is guaranteed.
2. Changes can be seen by us on fetch and also can still be rolledback.

---
what does deattached and expire object mean? It is not synchronized.

what is use of `session.begin()` apart from as a context manager where it automataically commits the session? Can we use it w/o context manager? How? 

---
explicitly rollingback is required on except, as partial completion of transaction is not allowed(atomicity)

    try:
        ...
        ...
        session.commit()
    except:
        session.rollback()      # necessary even after catching, otherwise in next statement, exception is again raised
    finally:
        ...

---
`session.get(User, 4)` get the item from identity map, if not present, it fetches from the DB. Nice method to get object based on primary key.

---
Once an object is fetched, it stays in identity map, new call to the object or even re-fetch with `session.query()` will give it from identity map only. 

However, if you need updated value from database, you need to manually `expire` or `refresh` the object. Then also, you will get latest value for object will depend on the **isolation level** you have set.

If isolation level is:

1. *Serialized*: Highest isolation level. Changes won't be visible in a session even after expiring the object.
2. *repeatable-read*: Once a object is read, re-fetching it after expiry will always give same object(even when it committed in another session). However, there is a problem of **phantom read**, i.e if it is deleted in other session, then it would be working on object which doesn't exist.
3. *read-committed*: If object committed to database, on re-fetching in a session, it will get the latest values. 

Problems: phantom read, non-repeatable read

3. *read-uncommitted*: lowest level, uncommitted but flushed changes will can be read by the session on re-fetching object after expiring it.

Problems: phantom read, non-repeatable read, dirty read(when other trans. can rollback this change later as it is not committed)

---
In a distributed database, two-phase commit is used to maintain consistency. First the databases prepare the table and rows to be committed(by applying a lock) then mutually they agree(by a leader or something) and commit.

---
`session.expunge(obj)` de-attaches object from session. So, it won't be synchronized with database(like flushing to DB, etc). Also, it won't be affected by session operations.

---
whenever abstracting some modification to database(add/update/delete) within a function 