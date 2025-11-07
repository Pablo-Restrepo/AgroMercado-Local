db = db.getSiblingDB("productos_db");

db.createUser({
  user: "admin",
  pwd: "admin123",
  roles: [{ role: "readWrite", db: "productos_db" }]
});

print("✅ Base de datos y usuario creados correctamente");

