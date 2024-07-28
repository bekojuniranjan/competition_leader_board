from pydantic import BaseModel
from typing import Optional

class Score(BaseModel):
    id: Optional[int]
    team_name: str
    accuracy_score: float
    precision_score: float
    recall_score: float
    f1_score: float
    roc_auc_score: float
    CrossEntropyLoss: float
    inference_time: float
    model_parameters_count: float    