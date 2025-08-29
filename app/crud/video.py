"""
비디오 CRUD 작업
"""
from sqlalchemy.orm import Session
from sqlalchemy import text

def get_videos(db: Session, skip: int = 0, limit: int = 100):
    sql_query = text("""
    SELECT
        f.feedid AS videoId,
        CASE
            WHEN f.promoKind = 'store' THEN s.storeName
            WHEN f.promoKind = 'product' THEN pf.productName
            WHEN f.promoKind = 'event' THEN ef.eventName
            ELSE f.body
        END AS videoName,
        f.mediaUrl AS videoUrl,
        f.created_at AS createdAt,
        f.body AS videoContent,
        h.imgUrl AS storeImage,
        COUNT(DISTINCT fl.userid) AS videoLikeCount,
        COUNT(DISTINCT r.reviewid) AS videoReviewCount
    FROM feed f
    JOIN store s ON f.storeid = s.storeid
    JOIN host h ON s.hostid = h.hostid
    LEFT JOIN productfeed pf ON f.feedid = pf.feedid
    LEFT JOIN eventfeed ef ON f.feedid = ef.feedid
    LEFT JOIN feedlike fl ON f.feedid = fl.feedid
    LEFT JOIN review r ON f.feedid = r.feedid
    WHERE f.mediaType = 'video'
    GROUP BY f.feedid, s.storeName, h.imgUrl, f.created_at, f.body, f.mediaUrl, f.promoKind, pf.productName, ef.eventName
    ORDER BY f.created_at DESC
    LIMIT :limit OFFSET :offset;
    """)
    
    result = db.execute(sql_query, {"limit": limit, "offset": skip}).mappings().all()
    return result
