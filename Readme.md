install 
flask
pymongo
pandas
pytorch
numpy
scikit-learn
mlflow
# Running the application
mlflow server --host 127.0.0.1 --port 8080
Quart
## run MongoDB
```bash
 sudo systemctl start mongod
 ```

### create a mongo user
in the mogodb shell
`bash use admin`
`bash db.createUser({ user: "fiot", pwd: "fiotdev123", roles: [ { role: "root", db: "admin" } ] })`


## run the application
```cd ./anlagenbetreiber```
```fiot start integration_test```