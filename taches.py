from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# l'instance de mon application
app = FastAPI(title = "Gestionnaires de taches: Todolist")

# ma liste python qui est comme ma base de data temporaire
taches = []

#class tache qui herite de BaseModel
class Tache(BaseModel):
    Id:int
    titre: str 
    description: Optional[str] = None
    statut: bool = True
    date: datetime = None

# repertoire racine
@app.get("/")
def root():
    return {"message": "Bienvenue sur notre application Todolist"}

# creer une tache
@app.post("/tache", response_model = Tache)
async def Creer_taches(tache : Tache):
    taches.append(tache)
    return tache

#lister toutes les taches
@app.get("/tache/touts", response_model = List[Tache])
def list_tache():
    return taches

#lister les taches en utilisant la pagination
@app.get("/tache/pagination", response_model = Tache )
def list_tache_pagination(debut: int = 0, limit: int = 5):
    return taches[debut: debut + limit]

#afficher une tache precise
@app.get("/tache/id/{id_tache}", response_model = Tache)
async def afficher_tache_precis(id_tache: int):
    for tache in taches:
        if tache.Id == id_tache:
            return {"message": f"tache a afficher est {tache}"}
    raise HTTPException(status_code = 404, detail  = "Item not found")

#afficher les taches faites
@app.get("/tache/etat/{statut_tache}", response_model = Tache)
def afficher_tache_faites(statut_tache: bool):
    tache_faite = [t for t in taches if t.statut == True]
    if not tache_faite:
        raise HTTPException(status_code = 404, detail  = "Item not found")
    return tache_faite


#afficher les taches non faites
@app.get("/tache/{statut_tache}", response_model = Tache)
def afficher_tache_non_faites(statut_tache: bool):
    taches_non_faites = [t for t in taches if t.statut == False]
    if not taches_non_faites:
        raise HTTPException(status_code = 404, detail  = "Item not found")
    return taches_non_faites

#afficher les taches faites en une date donnee
@app.get("/tache/date/{date_precis}", response_model = Tache)
def afficher_tache_faites_date_precise(date_precis: datetime):
    return [t for t in taches if t.date == date_precis]

#supprimer en utilisant l'ID
@app.delete("/tache/id/{id_tache}", response_model = Tache)
def supp_use_ID(id_tache: int):
    for tache in taches:
        if tache.Id == id_tache:
            taches.remove(tache)
            return {"message": "tache supprimee"}
    raise HTTPException(status_code=404, detail="tache non trouve")

#modifier en utilisant l'ID
@app.put("/tache/id/{id_tache}", response_model = Tache) 
def modifier_use_ID(id_tache: int, new_tache:Tache):
    for i,t  in enumerate(taches):
        if t.Id == id_tache:
            taches[i] = new_tache
            return taches[i]
    raise HTTPException(status_code=404, detail="tache non trouve")

#supprimer en utilisant le titre
@app.delete("/tache/titre/{titre_tache}", response_model = Tache)
def supp_use_titre(titre_tache: str, new_tache: Tache):
    for tache in taches:
        if tache.titre == titre_tache:
            taches.remove(tache)
            return {"message": f"tache {titre_tache} supprimee"} 
    raise HTTPException(status_code=404, detail="titre non trouve")

#modifier en utilisant le titre         
@app.put("/tache/{titre_tache}", response_model = Tache) 
def modifier_use_ID(titre_tache: str, new_tache:Tache):
    for i, tache in enumerate(taches):
        if tache.titre == titre_tache:
            taches[i] = new_tache
            return taches[i]
    raise HTTPException(status_code=404, detail="titre non trouve")

            




        

