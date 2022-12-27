from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import model
import orm
import repository
import services


orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_mariadb_uri()))
app = Flask(__name__)

# # 플라스크 앱 첫 번재 버전
# @app.route('/allocate', methods=['POST'])
# def allocate_endpoint():
#     session = get_session()
#     batches = repository.SqlAlchemyRepository(session).list()
#     line = model.OrderLine(
#         request.json['orderid']
#         , request.json['sku']
#         , request.json['qty']
#     )
    
#     batchref = model.allocate(line, batches)
    
#     return jsonify({'batchref': batchref}), 201


# 복잡해지기 시작하는 플라스크 앱
def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}

@app.route('/allocate', method=['POST'])
def allocate_endpoint():
    session = get_session()
    batches = repository.SqlAlchemyRepository(session).list()
    line = model.OrderLine(
        request.json['orderid']
        , request.json['sku']
        , request.json['qty']
    )
    
    if not is_valid_sku(line.sku, batches):
        return jsonify({'message': f'Invalid sku {line.sku}'}), 400
    
    try:
        batchref = model.allocate(line, batches)
    except model.OutOfStock as e:
        return jsonify({'message': str(e)}), 400
    
    session.commit()
    return jsonify({'batchref': batchref}), 201
                    


# @app.route("/allocate", methods=["POST"])
# def allocate_endpoint():
#     session = get_session()
#     repo = repository.SqlAlchemyRepository(session)
#     line = model.OrderLine(
#         request.json["orderid"], request.json["sku"], request.json["qty"],
#     )

#     try:
#         batchref = services.allocate(line, repo, session)
#     except (model.OutOfStock, services.InvalidSku) as e:
#         return {"message": str(e)}, 400

#     return {"batchref": batchref}, 201
