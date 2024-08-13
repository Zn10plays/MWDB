from connector import db
from connector.orm import Base

def init():
    session = db.get_session()

    try:
        Base.metadata.create_all(db.engine)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

if __name__ == '__main__':
    init()