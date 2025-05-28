from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.main.services.property_image_service import PropertyImageService

property_image_bp = Blueprint("property_image_bp", __name__, url_prefix="/api/images")

@property_image_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_image():
    data = request.get_json()
    return PropertyImageService.add_image(data)

@property_image_bp.route("/<int:property_id>", methods=["GET"])
@jwt_required()
def get_images(property_id):
    return PropertyImageService.get_images_by_property(property_id)
