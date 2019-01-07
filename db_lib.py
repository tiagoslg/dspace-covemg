import psycopg2


HOST = 'localhost'
DATABASE = 'dspace'
USER = 'dspace'
PASSWORD = 'dspace'


def get_conn():
    return psycopg2.connect(host=HOST,
                            database=DATABASE,
                            user=USER,
                            password=PASSWORD)


def close_conn(conn):
    return conn.close()


def get_internal_id(uuid):
    conn = get_conn()
    cur = conn.cursor()
    sql = """select internal_id from bitstream where bitstream.uuid = '{}'""".format(uuid)
    cur.execute(sql)
    internal_id = cur.fetchone()
    close_conn(conn)
    return internal_id


def get_file_type_size(uuid):
    conn = get_conn()
    cur = conn.cursor()
    sql = """
    select bfr.mimetype, b.size_bytes
    from bitstream as b
        inner join bitstreamformatregistry as bfr on bfr.bitstream_format_id = b.bitstream_format_id
    where internal_id = '{}'
    """.format(uuid)
    cur.execute(sql)
    ret = cur.fetchone()
    close_conn(conn)
    return ret
