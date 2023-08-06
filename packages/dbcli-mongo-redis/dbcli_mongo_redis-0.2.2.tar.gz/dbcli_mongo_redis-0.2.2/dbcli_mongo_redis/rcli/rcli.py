#!/usr/bin/env python3
import json

import click
import redis

js_edit_opts = {"require_save": False, "extension": ".js"}
txt_edit_opts = {"require_save": False, "extension": ".txt"}


def add_json_to_redis(cl, edited_doc, st=False, zst=False):
    data = json.loads(edited_doc)
    with cl.pipeline() as pipe:
        for key, value in data.items():
            if st:
                pipe.sadd(key, *value)
            elif zst:
                pipe.zadd(key, {value[0]: value[1]})
            elif isinstance(value, dict):
                pipe.hmset(key, value)
            elif isinstance(value, list):
                pipe.rpush(key, *value)
            else:
                pipe.set(key, value)
        pipe.execute()


def add_any_key_type(cl, edited_doc, key_type, key):
    data = edited_doc.split()
    if key_type == "string":
        cl.set(key, "".join(data))
    elif key_type == "bits":
        if len(data) != 2:
            raise click.ClickException("Bits data can contain only offset and value")
        else:
            cl.setbit(key, data[0], data[1])
    elif key_type == "list":
        cl.rpush(key, *data)
    elif key_type == "set":
        cl.sadd(key, *data)
    elif key_type == "sorted_set":
        dct = {}
        for i in range(1, len(data), 2):
            dct[data[i - 1]] = data[i]
        cl.zadd(key, dct)
    elif key_type == "hyll":
        cl.pfadd(key, *data)


def bytes_to_string(structure):
    new_dct = {}

    def a(data):
        if isinstance(data, (list, set, tuple)):
            res_list = []
            for item in data:
                if isinstance(item, (set, list, tuple, dict)):
                    res_list.append(a(item))
                else:
                    if isinstance(item, float):
                        res_list.append(item)
                    else:
                        res_list.append(item.decode("utf-8"))
            return res_list
        elif isinstance(data, dict):
            dct = {}
            for key, value in data.items():
                dct[key.decode("utf-8")] = a(value)
            return dct
        else:
            return data.decode("utf-8")

    for key, value in structure.items():
        new_dct[key.decode("utf-8")] = a(value)
    return new_dct


@click.group()
@click.option("-h", "--host", default="localhost", help="Redis host.")
@click.option("-p", "--port", default=6379, help="Redis port.")
@click.option("-d", "--db", default=0, help="Database number.")
@click.pass_context
def cli(ctx, host, port, db):
    ctx.ensure_object(dict)
    ctx.obj["RedisClient"] = redis.Redis(host=host, port=port, db=db)
    return ctx.obj["RedisClient"]


@cli.command()
@click.pass_context
def db_count():
    """Show count of db"""
    cl = redis.StrictRedis()
    print(cl.config_get("databases"))


@cli.command()
@click.option("-p", "--pattern", default="*", help="Keys search pattern.")
@click.pass_context
def list_keys(ctx, pattern):
    """Show all keys in db(uft-8 format)"""
    cl = ctx.obj["RedisClient"]
    keys = [key.decode("utf-8") for key in cl.keys(pattern=(pattern + "*"))]
    print(*keys, sep="\n")


@cli.command()
@click.option("-k", "--key", default=None, help="Document key.")
@click.option("-p", "--pattern", default="*", help="Keys search pattern.")
@click.pass_context
def show_db(ctx, key, pattern):
    """Show data in 'key: value' format"""
    cl = ctx.obj["RedisClient"]
    if key:
        keys_list = [key.encode("utf-8")]
    else:
        keys_list = cl.keys(pattern=pattern)
    # check key type and get key's value
    for key in keys_list:
        if cl.type(key) == b"string":
            print(key, ": ", cl.get(key))
        elif cl.type(key) == b"hash":
            print(key, ": ", cl.hgetall(key))
        elif cl.type(key) == b"list":
            print(key, ": ", cl.lrange(key, 0, -1))
        elif cl.type(key) == b"set":
            print(key, ": ", cl.smembers(key))
        elif cl.type(key) == b"zset":
            print(key, ": ", cl.zrange(key, 0, -1, withscores=True))
        else:
            print("Unsupported value in key: ", key)


@cli.command()
@click.argument("key")
@click.option("-b", "--bits/--no-bits", default=False, help="Bits type key")
@click.option("-l", "--lst/--no-lst", default=False, help="List type key")
@click.option("-h", "--hsh/--no-hsh", default=False, help="Hash type key")
@click.option("-s", "--st/--no-st", default=False, help="Set type key")
@click.option("-z", "--sset/--no-sset", default=False, help="Sorted set type key")
@click.option("-e", "--hyll/--no-hyll", default=False, help="HyperLogLog type key")
@click.pass_context
def add_key(ctx, key, bits, lst, hsh, st, sset, hyll):
    """Add key to db. Don't support streams and geo"""
    cl = ctx.obj["RedisClient"]
    key_type = None
    types_dict = {
        "bits": bits,
        "list": lst,
        "set": st,
        "hsh": hsh,
        "sorted_set": sset,
        "hyll": hyll,
    }
    for ke, value in types_dict.items():
        if value:
            if key_type is None:
                key_type = ke
            else:
                raise click.ClickException("Only one key type can be set")
    if key_type is None:
        key_type = "string"
    # open txt-editor
    if key_type == "hsh":
        new_doc = {"key1": "value1", "key2": "value2"}
        edited_doc = click.edit(json.dumps(new_doc, indent=4), **js_edit_opts)
        if edited_doc:
            try:
                add_json_to_redis(cl, json.dumps({key: json.loads(edited_doc)}))
            except Exception as ex:
                print("Key was not added: ", ex)
    # open json-editor.
    elif key_type:
        new_doc = "value"
        edited_doc = click.edit(new_doc, **txt_edit_opts)
        if edited_doc:
            try:
                add_any_key_type(cl, edited_doc, key_type, key)
            except Exception as ex:
                print("Key was not added: ", ex)
    else:
        print(key_type)
        raise click.ClickException("Key type should be set")


@cli.command()
@click.pass_context
def add_data(ctx):
    """Add json-format data to db"""
    cl = ctx.obj["RedisClient"]
    new_doc = {"key1": "value1", "key2": "value2"}
    edited_doc = click.edit(json.dumps(new_doc, indent=4), **js_edit_opts)
    if edited_doc:
        try:
            add_json_to_redis(cl, edited_doc)
        except Exception as ex:
            print("Key was not added: ", ex)


@cli.command()
@click.option("-k", "--key", help="Document key.")
@click.pass_context
def edit_doc(ctx, key):
    """Open document in editor. Support only json-format"""
    cl = ctx.obj["RedisClient"]
    st = False
    zst = False
    if cl.type(key) == b"string":
        try:
            new_doc = {key: cl.get(key).decode("utf-8")}
        except UnicodeDecodeError:
            raise click.ClickException("HyperLogLog cant be edited")
    elif cl.type(key) == b"list":
        new_doc = bytes_to_string({key.encode("utf-8"): cl.lrange(key, 0, -1)})
    elif cl.type(key) == b"set":
        st = True
        new_doc = bytes_to_string({key.encode("utf-8"): cl.smembers(key)})
    elif cl.type(key) == b"hash":
        new_doc = bytes_to_string({key.encode("utf-8"): cl.hgetall(key)})
    elif cl.type(key) == b"zset":
        zst = True
        new_doc = bytes_to_string(
            {key.encode("utf-8"): cl.zrange(key, 0, -1, withscores=True)}
        )
    else:
        raise click.ClickException(
            f'Wrong key: "{key}" or unsupported key type: "{cl.type(key)}"'
        )
    edited_doc = click.edit(
        json.dumps(new_doc, indent=4), require_save=True, extension=".js"
    )
    if edited_doc:
        cl.delete(key)
        try:
            add_json_to_redis(cl, edited_doc, st=st, zst=zst)
        except Exception as ex:
            print("Key was not edited: ", ex)
            add_json_to_redis(cl, json.dumps(new_doc), st=st, zst=zst)


@cli.command()
@click.option("-k", "key", help="Document key.")
@click.pass_context
def del_doc(ctx, key):
    """Delete key from db"""
    cl = ctx.obj["RedisClient"]
    cl.delete(key)


@cli.command()
@click.option("-k", "key", help="Document key.")
@click.pass_context
def to_set(ctx, key):
    """Turn redis list to set"""
    cl = ctx.obj["RedisClient"]
    if cl.type(key) == b"list":
        data = cl.lrange(key, 0, -1)
        cl.delete(key)
        cl.sadd(key, *data)
    else:
        raise click.ClickException(
            f'Wrong key type: "{cl.type(key)}". Argument should be b"list"'
        )


@cli.command()
@click.option("-k", "key", help="Document key.")
@click.pass_context
def to_zset(ctx, key):
    """Turn redis hash into sorted set"""
    cl = ctx.obj["RedisClient"]
    if cl.type(key) == b"hash":
        data = cl.hgetall(key)
        cl.delete(key)
        cl.zadd(key, data)
    else:
        raise click.ClickException(
            f'Wrong key type: "{cl.type(key)}". Argument should be b"hash"'
        )


def _main():
    cli(obj={})


if __name__ == "__main__":
    _main()
