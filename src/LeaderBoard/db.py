import sqlite3

import sqlite3
from models import Score


class Database:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("data/data.db")
        print("Opened Database Successfully")
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scores
                    (
                        id INTEGER  PRIMARY KEY AUTOINCREMENT,
                        team_name TEXT NOT NULL,
                        accuracy_score REAL,
                        precision_score REAL,
                        recall_score REAL,
                        f1_score REAL,
                        roc_auc_score REAL,
                        CrossEntropyLoss REAL,
                        inference_time REAL,
                        model_parameters_count REAL
                    );
        """
        )

    def insert_row(self, score: Score):
        sql = "INSERT INTO scores (team_name, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, CrossEntropyLoss, inference_time, model_parameters_count) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' );".format(
            str(score.team_name), str(score.accuracy_score), str(score.precision_score), str(score.recall_score), str(score.f1_score), str(score.roc_auc_score), str(score.CrossEntropyLoss), str(score.inference_time), str(score.model_parameters_count)
        )
        self.conn.execute(sql)
        self.conn.commit()

    def get_all_employees(self):
        return [dict(zip(['id', 'team_name', 'accuracy_score', 'precision_score', 'recall_score', 'f1_score', 'roc_auc_score', 'CrossEntropyLoss', 'inference_time', 'model_parameters_count'], row)) for row in self.conn.execute("SELECT * from scores")]

    def get_employee_by_id(self, id):
        return [dict(zip(['id', 'team_name', 'accuracy_score', 'precision_score', 'recall_score', 'f1_score', 'roc_auc_score', 'CrossEntropyLoss', 'inference_time', 'model_parameters_count'], row)) for row in self.conn.execute(f"SELECT * from scores where id = {id}")]

    def delete_row(self, id):
        self.conn.execute(f"DELETE from scores where id = {id}")
        self.conn.commit()

    def update_row(self, score_id: int, column: str, new_value: str | int):
        sql = f"UPDATE scores set {column} = '{new_value}' where id = {score_id}"
        self.conn.execute(sql)
        self.conn.commit()

if __name__ == "__main__":
    database = Database()