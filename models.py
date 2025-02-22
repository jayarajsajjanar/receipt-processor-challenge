"""
This module defines the SQLAlchemy models for the application.

Classes:
    Receipt: Represents a purchase receipt.
    Item: Represents an item in a receipt.
"""

# from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy  # pylint:disable=import-error

db = SQLAlchemy()


# pylint:disable=too-few-public-methods
class Receipt(db.Model):  # type: ignore
    """
    Represents a purchase receipt.

    Attributes:
        id (str): The unique identifier for the receipt.
        retailer (str): The name of the retailer.
        purchaseDate (date): The date of the purchase.
        purchaseTime (time): The time of the purchase.
        total (str): The total amount of the purchase.
        items (list[Item]): The list of items in the receipt.
        points (float): Total points based on request data.
    """

    # id = db.Column(db.String, nullable=False, default=str(uuid4()),
    # primary_key=True)
    id = db.Column(db.String, nullable=False, primary_key=True)
    retailer = db.Column(db.String, nullable=False)
    purchaseDate = db.Column(db.String, nullable=False)
    purchaseTime = db.Column(db.String, nullable=False)
    total = db.Column(db.Float, nullable=False)
    items = db.relationship("Item", backref="receipt", lazy=True)
    # points = db.Column(db.Float, default=0, nullable=False)
    points = db.Column(db.Integer, default=0, nullable=False)


class Item(db.Model):  # type: ignore # pylint:disable=too-few-public-methods
    """
    Represents an item in a receipt.

    Attributes:
        id (int): The unique identifier for the item.
        receipt_id (str): The identifier of the receipt this item belongs to.
        short_description (str): A short description of the item.
        price (str): The price of the item.
    """

    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(
        db.String, db.ForeignKey("receipt.id"), nullable=False
    )  # noqa: E501
    shortDescription = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)


# class Points(db.Model):
#     """
#     Represents the points earned from a receipt.

#     Attributes:
#         id (int): The unique identifier for the points.
#         receipt_id (str): The identifier of the receipt
# these points belong to.
#         points (int): The number of points earned.
#     """

#     id = db.Column(db.Integer, primary_key=True)
#     receipt_id = db.Column(
# db.String, db.ForeignKey("receipt.id"), nullable=False
#     )
#     points = db.Column(db.Integer, nullable=False)
#     # generated_by_llm = db.Column(db.Boolean, nullable=False, default=False)
