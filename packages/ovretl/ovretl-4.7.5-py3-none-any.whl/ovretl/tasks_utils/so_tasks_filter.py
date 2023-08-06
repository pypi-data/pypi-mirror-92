import pandas as pd


def so_tasks_filter(tasks_df: pd.DataFrame) -> pd.DataFrame:
    so_tasks_df = tasks_df.loc[tasks_df["so_id"].notnull(), :]
    so_tasks_df.loc[:, "created_at"] = so_tasks_df["created_at"].dt.date
    so_tasks_df.loc[:, "updated_at"] = so_tasks_df["updated_at"].dt.date
    so_tasks_df.loc[:, "due_date"] = so_tasks_df["due_date"].dt.date
    so_tasks_df.loc[:, "done_date"] = so_tasks_df["done_date"].dt.date
    return so_tasks_df
