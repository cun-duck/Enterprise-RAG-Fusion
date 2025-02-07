from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import pandas as pd

class EnterpriseDBConnector:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.metadata = MetaData()
        self.Session = sessionmaker(bind=self.engine)
        
    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
            
    def query_to_dataframe(self, query: str) -> pd.DataFrame:
        return pd.read_sql(query, self.engine)
    
    def write_dataframe(self, df: pd.DataFrame, table_name: str):
        df.to_sql(
            name=table_name,
            con=self.engine,
            if_exists="append",
            index=False
        )
