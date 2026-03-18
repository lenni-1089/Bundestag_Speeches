from dbt.cli.main import dbtRunner, dbtRunnerResult

# initialize
dbt = dbtRunner()

DBT_PROJECT_PATH = "/Workspace/Users/rosenthal.lennart@gmail.com/Bundestag_Speeches/bundestag_dbt"

# pull all relevant dbt dependencies
# not relevant for our current project status as our dbt models
# do not yet use any packages, but might be relevant when
# extending or using dbt packages like db_utils later

cli_deps = ["deps","--project-dir", DBT_PROJECT_PATH]

# invoking a dbt run of all models
cli_run = ["run","--project-dir", DBT_PROJECT_PATH]

# invoking tests on all models
cli_test = ["test","--project-dir", DBT_PROJECT_PATH]

# run the command
print("Running dbt deps...")

res_deps: dbtRunnerResult = dbt.invoke(cli_deps)

if res_deps.success == False and res_deps.result:
    print(f"Dbt dependency error: {res_deps.result})
    
          
print("Running dbt models...")


res_run: dbtRunnerResult = dbt.invoke(cli_run)

    print(f"Dbt run error: {e}")
          
print("Running dbt tests...")


    res_test: dbtRunnerResult = dbt.invoke(cli_test)
except Exception as e:
    print(f"Dbt test error: {e}")


# inspect the results
for r in res.result:
    print(f"{r.node.name}: {r.status}")