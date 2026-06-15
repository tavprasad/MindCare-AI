from fastapi import FastAPI
from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated
from fastapi.responses import JSONResponse
import pickle
import pandas as pd

with open("model1.pkl",'rb') as f:
    model=pickle.load(f)


app=FastAPI()

class UserInput(BaseModel):
    Gender:Annotated[Literal['Male','Female'],Field(...,description="Gender of the Student")]
    Age:Annotated[int,Field(...,gt=17,lt=35,description="Age of the Student")]
    Academic_Pressure:Annotated[int,Field(...,gt=0,lt=6,description="Academic Pressure on Student")]
    Study_Satisfaction:Annotated[int,Field(...,gt=0,lt=6,description="Study Satisfaction of the Student")]
    Sleep_Duration:Annotated[Literal['7-8 hours','More than 8 hours','5-6 hours','Less than 5 hours'],Field(..., description="Sleep Duration of the Student")]
    Dietary_Habits:Annotated[Literal['Moderate','Unhealthy','Healthy'],Field(...,description="Diet of Student")]
    Suicidial_thoughts:Annotated[Literal['Yes','No'],Field(...,description='Suicial thoughts')]
    Study_hours:Annotated[int,Field(...,gte=0,lt=13,description="Study hours of student")]
    Financial_Stress:Annotated[int,Field(...,gt=0,lt=6,description="Financial Stress of Student")]
    Family_history:Annotated[Literal['Yes','No'],Field(...,description="Hereditary problem to Student?")]


    @computed_field
    @property
    def Stress_index(self)->int:
        return self.Academic_Pressure + self.Financial_Stress
    
    @computed_field
    @property
    def Lifestyle_Score(self) -> int:

        sleep_map = {
            "Less than 5 hours": 1,
            "5-6 hours": 2,
            "7-8 hours": 3,
            "More than 8 hours": 4
        }

        diet_map = {
            "Unhealthy": 0,
            "Moderate": 1,
            "Healthy": 2
        }

        return (
            sleep_map[self.Sleep_Duration]
            + self.Study_Satisfaction
            + diet_map[self.Dietary_Habits]
        )

@app.get("/")
def home():
    return {
        'message':'MindCare AI API running'
    }

@app.post('/predict')
def predict(data: UserInput):
    

    gender_map={"Male":1,"Female":0}

    sleep_map={
            'Less than 5 hours':1,
            '5-6 hours':2,
            '7-8 hours':3,
            'More than 8 hours':4
        }

    dietary_map={
            'Unhealthy':0,
            'Moderate':1,
            'Healthy':2
        }

    suicidal_map={
            "Yes":1,
            "No":0
        }

    family_map={
            "Yes":1,
            "No":0
        }


    input_df=pd.DataFrame([{
        'Gender':gender_map[data.Gender],
        'Age':data.Age,
        'Academic Pressure':data.Academic_Pressure,
        'Study Satisfaction':data.Study_Satisfaction,
        'Sleep Duration':sleep_map[data.Sleep_Duration],
        'Dietary Habits':dietary_map[data.Dietary_Habits],
        'Have you ever had suicidal thoughts ?':suicidal_map[data.Suicidial_thoughts],
        'Study Hours':data.Study_hours,
        'Financial Stress':data.Financial_Stress,
        'Family History of Mental Illness':family_map[data.Family_history],
        'Stress_index':data.Stress_index,
        'Lifestyle_Score':data.Lifestyle_Score
    }])

    prediction = model.predict(input_df)[0]


    return JSONResponse(
        status_code=200,
        content={
            "Predicted_category": int(prediction)
        }
    )