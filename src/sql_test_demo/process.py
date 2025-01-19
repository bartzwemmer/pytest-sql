from pathlib import Path
from time import sleep

def get_sql_query(sql_file: Path) -> str:
    with sql_file.open() as f:
        return f.read()
    
def deploy_function(sql_file: Path) -> None:
    print(f"SQL function created successfully from SQL file {sql_file}!")
    
if __name__ == "__main__":
    print("Starting Prefect Flow")
    print("Doing things")
    sleep(5)
    deploy_function(Path("sql/format_pc_wpl.sql"))
    print("Doing more things")
    print("Finished Prefect Flow")