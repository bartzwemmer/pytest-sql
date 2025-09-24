from pathlib import Path

import pandas as pd
from sqlalchemy import Engine, text
from sqlalchemy.schema import DDL

from sql_test_demo.process import get_sql_query


def test_create_table(db: Engine):
    """
    Demo test with SQL DDL
    """
    print("Test if table exists")
    select_stmt = text("SELECT * FROM format_pc_wpl('1234AB', 'Duckstad')")
    query = get_sql_query(Path("sql/format_pc_wpl.sql"))

    with db.connect() as conn:
        # Create function in database, don't commit so we have a clean database afterwards
        conn.execute(DDL(query))
        res = conn.execute(select_stmt).fetchall()[0]  # return first row
    assert res == ("1234AB Duckstad",)


def test_some_query(db: Engine):
    """
    Demo test with a DataFrame for the test data
    """
    print("Test SQL query")
    # Dataframe with test data
    d = {"col1": [1, 2], "col2": [3, 4]}
    df = pd.DataFrame(data=d)
    df.to_sql("test", con=db.connect(), if_exists="replace", index=False, chunksize=10)
    with db.connect() as conn:
        res = conn.execute(text("SELECT * FROM test")).fetchall()
        # clean up after test
        print("Since we created the table manually outside of SQLAlchemy, we need to clean this table up.")
        conn.execute(text("""DROP TABLE "test" """))
        conn.commit()
        print("Manual table deleted.")

    assert res == [(1, 3), (2, 4)]
