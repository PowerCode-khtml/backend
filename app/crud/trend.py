from sqlalchemy.orm import Session
from sqlalchemy import text

def get_store_rankings(db: Session, limit: int = 10):
    sql_query = text(f"""
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
    LIMIT {limit}
    """)
    
    result = db.execute(sql_query).mappings().all()
    return result

def get_product_rankings(db: Session, limit: int = 10):
    sql_query = text(f"""
    SELECT
	        bp.mediaUrl,
	        bp.productName,
	        bp.like_count,
	        (
	            SELECT COUNT(DISTINCT x.like_count) + 1
	            FROM (
	                SELECT f2.feedid, COUNT(fl2.userid) AS like_count
	                FROM feed f2
	                LEFT JOIN feedlike fl2 ON fl2.feedid = f2.feedid
	                WHERE f2.promoKind = 'product'
	                GROUP BY f2.feedid
	            ) x
	            WHERE x.like_count > bp.like_count
	        ) AS `rank`
	    FROM (
	        SELECT
	            f.feedid,
	            f.mediaUrl,
	            -- ONLY_FULL_GROUP_BY 환경에서도 안전하게: PK 종속 컬럼은 MAX로 취함
	            MAX(p.productName) AS productName,
	            COUNT(fl.userid) AS like_count
	        FROM feed f
	        JOIN product_feed pf ON pf.feedid = f.feedid
            JOIN product p ON p.productid = pf.productid
	        LEFT JOIN feedlike fl ON fl.feedid = f.feedid
	        WHERE f.promoKind = 'product'
	        GROUP BY f.feedid, f.mediaUrl
	    ) bp
	    ORDER BY bp.like_count DESC, bp.feedid ASC
	    LIMIT {limit};
    """)

    result = db.execute(sql_query).mappings().all()
    return result

def get_event_rankings(db: Session, limit: int = 10):
    sql_query = text(f"""
    SELECT
        be.eventName,
        be.imgUrl,
        be.like_count,
        (
            SELECT COUNT(DISTINCT x.like_count) + 1
            FROM (
                SELECT f2.feedid, COUNT(fl2.userid) AS like_count
                FROM feed f2
                LEFT JOIN feedlike fl2 ON fl2.feedid = f2.feedid
                WHERE f2.promoKind = 'event'
                GROUP BY f2.feedid
            ) x
            WHERE x.like_count > be.like_count
        ) AS `rank`
    FROM (
        SELECT
            f.feedid,
            MAX(ef.eventName) AS eventName,
            MAX(ef.imgUrl)    AS imgUrl,
            COUNT(fl.userid)  AS like_count
        FROM feed f
        JOIN eventfeed ef ON ef.feedid = f.feedid
        LEFT JOIN feedlike fl ON fl.feedid = f.feedid
        WHERE f.promoKind = 'event'
        GROUP BY f.feedid
    ) be
    ORDER BY be.like_count DESC, be.feedid ASC
    LIMIT {limit};
    """)
    result = db.execute(sql_query).mappings().all()
    return result
