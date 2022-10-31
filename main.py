from fastapi import FastAPI, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import Team, TeamView
from database import init_db
import pandas as pd

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def start_db():
    await init_db()


@app.get("/")
async def root():
    # return {"message": "Hello World"}
    teams = await Team.find_all().project(TeamView).to_list()
    return teams


@app.get("/team/{team_name}")
async def get_team(team_name: str):
    team = await Team.find_one(Team.name == team_name).project(TeamView)
    return team.ranking


@app.get("/top/")
async def get_top():
    res = await Team.find({"ranking.Week 06": {"$lt": 6}}) \
        .project(TeamView) \
        .sort("+ranking.Week 06") \
        .to_list()
    return [team.name for team in res]


@app.get("/files/", response_class=HTMLResponse)
async def view_update(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/files/")
# Using def as fastapi will send it to a threadpool
# https://fastapi.tiangolo.com/async/#path-operation-functions
async def upload_files(file: UploadFile):
    df = read_csv(file.file)
    week = list(df)[0]
    team: Team
    async for team in Team.find():
        val = int(df.loc[team.name][0])
        await team.update({"$set": {f"ranking.{week}": val}})
    await file.close()


def read_csv(file):
    df: pd.DataFrame = pd.read_csv(file)
    df = df.rename(columns={"team": "name"}).set_index("name")
    return df
