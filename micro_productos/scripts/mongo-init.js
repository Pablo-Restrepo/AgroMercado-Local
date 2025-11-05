db = db.getSiblingDB(process.env.MONGO_DB || "productos_db");

db.createUser({
  user: process.env.MONGO_USER,
  pwd: process.env.MONGO_PASSWORD,
  roles: [{ role: "readWrite", db: process.env.MONGO_DB || "productos_db" }]
});

print("✅ Base de datos y usuario creados correctamente");
