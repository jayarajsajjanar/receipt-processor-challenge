"""Main application file."""

from uuid import uuid4

from flask import Flask, request  # pylint:disable=import-error

from log import log_request, logger
from models import Item, Receipt, db  # noqa: F403, F401
from utils import calculate_points, handle_error, validate_request

app = Flask(__name__)

# todo: Use the newer Declarative style  # pylint:disable=fixme
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example2.db"

db.init_app(app)  # noqa: F405

with app.app_context():
    # logger.info("Dropping tables")
    # db.drop_all()
    logger.info("Creating tables")
    db.create_all()  # noqa: F405


@app.route("/")
@log_request
def root_debug():
    """Root endpoint for debugging."""
    return "Hello World3!"


@app.route("/receipts/process", methods=["POST"])
@handle_error  # 500 error
def process_receipt():
    """Process receipt data and calculate points."""
    data = request.get_json()
    try:
        validate_request(data)
    except Exception as e:  # pylint:disable=broad-exception-caught
        logger.error("The receipt is invalid: %s \n %s", e, data)
        return "The receipt is invalid", 400

    # noqa: F405
    receipt = Receipt(  # noqa: F405
        id=str(uuid4()),
        retailer=data["retailer"],
        # purchaseDate=datetime.strptime(
        #     data["purchaseDate"], "%Y-%m-%d"
        # ).date(),  # noqa: E501
        purchaseDate=data["purchaseDate"],
        # purchaseTime=datetime.strptime(data["purchaseTime"], "%H:%M").time(),
        total=float(data["total"]),
        purchaseTime=data["purchaseTime"],
        items=[
            Item(  # noqa: F405
                shortDescription=item["shortDescription"],
                price=float(item["price"]),  # noqa: F405
            )
            for item in data["items"]
        ],
        points=0,
    )

    points = calculate_points(
        receipt.retailer,
        receipt.total,
        [
            {"shortDescription": item.shortDescription, "price": item.price}
            for item in receipt.items
        ],
        receipt.purchaseDate,
        receipt.purchaseTime,
        data.get("generated_by_llm", False),
    )

    receipt.points = points

    db.session.add(receipt)  # noqa: F405
    db.session.commit()  # noqa: F405

    return {"id": receipt.id}, 200


@app.route("/receipts/<receipt_id>/points", methods=["GET"])
@handle_error  # 500 error
def get_points(receipt_id):
    """Get the points for a receipt."""
    receipt = Receipt.query.get(receipt_id)  # noqa: F405
    if not receipt:
        return "No receipt found for that ID.", 404

    return {"points": receipt.points}, 200


if __name__ == "__main__":
    """Run the app."""  # pylint:disable=pointless-string-statement
    app.run(debug=True, host="0.0.0.0", port="8000")
