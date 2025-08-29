import pymysql

def fetch_popular_stores_rank(conn, limit=10):
    sql = f"""
    SELECT
        bs.storeName,
        bs.imgUrl,
        -- dense rank: 현재 점수보다 큰 '서로 다른 점수'의 개수 + 1
        (SELECT COUNT(DISTINCT bs2.score) + 1
           FROM (
                SELECT
                    s2.storeid,
                    (COALESCE(subs2.cnt, 0) + COALESCE(likes2.cnt, 0)) AS score
                FROM store s2
                LEFT JOIN (
                    SELECT storeid, COUNT(*) AS cnt
                    FROM subscription
                    GROUP BY storeid
                ) subs2 ON subs2.storeid = s2.storeid
                LEFT JOIN (
                    SELECT f2.storeid, COUNT(fl2.userid) AS cnt
                    FROM feed f2
                    LEFT JOIN feedlike fl2 ON fl2.feedid = f2.feedid
                    WHERE f2.promoKind = 'store'
                    GROUP BY f2.storeid
                ) likes2 ON likes2.storeid = s2.storeid
           ) bs2
          WHERE bs2.score > bs.score
        ) AS `rank`
    FROM (
        -- 점포별 점수 계산 (구독수 + 점포홍보 좋아요수)
        SELECT
            s.storeid,
            s.storeName,
            h.imgUrl,
            (COALESCE(subs.cnt, 0) + COALESCE(likes.cnt, 0)) AS score
        FROM store s
        JOIN host h ON h.hostid = s.hostid
        LEFT JOIN (
            SELECT storeid, COUNT(*) AS cnt
            FROM subscription
            GROUP BY storeid
        ) subs ON subs.storeid = s.storeid
        LEFT JOIN (
            SELECT f.storeid, COUNT(fl.userid) AS cnt
            FROM feed f
            LEFT JOIN feedlike fl ON fl.feedid = f.feedid
            WHERE f.promoKind = 'store'
            GROUP BY f.storeid
        ) likes ON likes.storeid = s.storeid
    ) bs
    ORDER BY bs.score DESC, bs.storeid ASC
    LIMIT {limit};
    """
    with conn.cursor(pymysql.cursors.DictCursor) as cur:
        cur.execute(sql)
        rows = cur.fetchall()

    return [
        {"rank": int(r["rank"]), "storeName": r["storeName"], "imgUrl": r["imgUrl"]}
        for r in rows
    ]
