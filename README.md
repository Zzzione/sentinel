# sentinel

AAA module

API usage:

Register new user: curl -X POST http://localhost:8000/register   -H "Content-Type: application/json"   -d '{"username":"matthew","email":"matthew@example.com","password":"supersecret"}'\n
Create new role: curl -X POST http://localhost:8000/roles      -H "Content-Type: application/json"      -d '{"name":"admin","description":"Administrator role"}'\n
Assign role: curl -X POST http://localhost:8000/users/1/roles      -H "Content-Type: application/json"      -d '{"role_id": 1, "user_id": 1}'\n
Show user role: curl -X GET http://localhost:8000/users/1/roles\n
