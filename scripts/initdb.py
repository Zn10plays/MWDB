from connector import db
from connector.orm import Base
from minio import Minio
import os
import dotenv

dotenv.load_dotenv()


def init():
    init_sql_db()
    init_minio()
    pass

def init_minio():
    client = Minio('localhost:'+os.environ.get('MINIO_PORT'),
                access_key=os.environ.get('MINIO_ROOT_USER'),
                secret_key=os.environ.get('MINIO_ROOT_PASSWORD'),
                secure=False)
    try:
        if not client.bucket_exists('novels'):
            client.make_bucket('novels')
    except Exception as e:
        print(f'failed to create minio bucket: {e}')
        pass
    pass

def init_sql_db():
    session = db.get_session()

    try:
        Base.metadata.create_all(db.engine)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

    pass

if __name__ == '__main__':
    init()