from fastapi import FastAPI
from app.models import Snack
from app.database.supabase import create_supabase_client

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Initialize supabase client
supabase = create_supabase_client()

def snack_exists(key: str = "name", value: str = None):
    snack = supabase.from_("snacks").select("*").eq(key, value).execute()
    return len(snack.data) > 0

# Create a new snack
@app.post("/snacks")
def create_snack(snack: Snack):
    try:
        # Add snack to snacks table
        snack = supabase.from_("snacks")\
            .insert({"name": snack.name, "description": snack.description})\
            .execute()

        # Check if snack was added
        if snack:
            return {"message": "Snack created successfully"}
        else:
            return {"message": "Snack creation failed"}
    except Exception as e:
        print("Error: ", e)
        return {"message": "Snack creation error"}

@app.get('/snacks')
def read_snacks():
    try:
        snacks = supabase.from_("snacks")\
                    .select("id", "name", "description")\
                    .execute()
        
        if snacks:
            return snacks
        
    except Exception as e:
        print("Error: ", e)
        return {"message": "Snack creation error"}
    
@app.get('/snacks/{snack_id}')
def read_snack(snack_id: str):
    try:
        snack = supabase.from_("snacks")\
            .select("id", "name", "description")\
            .eq("id", snack_id)\
            .execute()

        if snack:
            return snack
        
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Snack not found"}
    
# Delete a snack
@app.delete("/snacks/{snack_id}")
def delete_snack(snack_id: str):
    try:        
        # Check if snack exists
        if snack_exists("id", snack_id):
            # Delete snack
            supabase.from_("snacks")\
                .delete().eq("id", snack_id)\
                .execute()
            return {"message": "Snack deleted successfully"}

        else:
            return {"message": "Snack deletion failed"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Snack deletion failed"}
    
# Update a snack
@app.put("/snacks/{snack_id}")
def update_snack(snack_id: str, snack: Snack):
    try:
        # Update snack
        snack_record = supabase.from_("snacks")\
            .update({"name": snack.name, "description": snack.description})\
            .eq("id", snack_id).execute()
        if snack_record:
            return {"message": "Snack updated successfully"}
        else:
            return {"message": "Snack update failed"}
    except Exception as e:
        print(f"Error: {e}")
        return {"message": "Snack update failed"}
    

# Add CORS after routes
origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://nuxt-snacks.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)