import json

Hypothesis_no = 4

SEMANTIC_DATABASE_FILE = f"./Hypothesis_{Hypothesis_no}/world_frame_set_1_hypoth{Hypothesis_no}.txt"
SEMANTIC_DATABASE_AVERAGE_FILE = f"./Hypothesis_{Hypothesis_no}/world_frame_set_1_average_hypoth{Hypothesis_no}.txt"
database_entries = {}
with open(SEMANTIC_DATABASE_FILE, "r") as f:
    for line in f:
        database_entry = json.loads(line)
        if database_entry["Name"] in database_entries:
            if database_entry["Corner_name"] not in database_entries[database_entry["Name"]]:
                database_entries[database_entry["Name"]][database_entry["Corner_name"]] = {}
                database_entries[database_entry["Name"]][database_entry["Corner_name"]]["X"] = database_entry["X"]
                database_entries[database_entry["Name"]][database_entry["Corner_name"]]["Y"] = database_entry["Y"]
                database_entries[database_entry["Name"]][database_entry["Corner_name"]]["Z"] = database_entry["Z"]
                database_entries[database_entry["Name"]][database_entry["Corner_name"]]["count"] = 1
            else:
                database_entries[database_entry["Name"]][database_entry["Corner_name"]]["X"] = (
                    database_entries[database_entry["Name"]][database_entry["Corner_name"]]["X"]
                    * database_entries[database_entry["Name"]][database_entry["Corner_name"]]["count"]
                    + database_entry["X"]
                ) / (database_entries[database_entry["Name"]][database_entry["Corner_name"]]["count"] + 1)
                database_entries[database_entry["Name"]][database_entry["Corner_name"]]["Y"] = (
                    database_entries[database_entry["Name"]][database_entry["Corner_name"]]["Y"]
                    * database_entries[database_entry["Name"]][database_entry["Corner_name"]]["count"]
                    + database_entry["Y"]
                ) / (database_entries[database_entry["Name"]][database_entry["Corner_name"]]["count"] + 1)
                database_entries[database_entry["Name"]][database_entry["Corner_name"]]["Z"] = (
                    database_entries[database_entry["Name"]][database_entry["Corner_name"]]["Z"]
                    * database_entries[database_entry["Name"]][database_entry["Corner_name"]]["count"]
                    + database_entry["Z"]
                ) / (database_entries[database_entry["Name"]][database_entry["Corner_name"]]["count"] + 1)
                database_entries[database_entry["Name"]][database_entry["Corner_name"]]["count"] += 1

        else:
            database_entries[database_entry["Name"]] = {}
    f.close()

with open(SEMANTIC_DATABASE_AVERAGE_FILE, "w") as f:
    json.dump(database_entries, f, indent=4)
    f.close()
