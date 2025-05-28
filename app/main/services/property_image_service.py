from app.main.models.property_image import PropertyImage
from app.main.schema.property_image_schema import PropertyImageSchema
from app.main.extensions import db
from app.main.utils.response import success_response, error_response



class PropertyImageService:
    @staticmethod
    def add_image(data):
        schema = PropertyImageSchema()
        try:
            validated_data = schema.load(data)

            image = PropertyImage(
                property_id=validated_data['property_id'],
                image_url=validated_data['image_url']
            )
            db.session.add(image)
            db.session.commit()

            return success_response("Image uploaded successfully", schema.dump(image))
        except Exception as e:
            db.session.rollback()
            return error_response(f"Failed to upload image: {str(e)}", 500)

    @staticmethod
    def get_images_by_property(property_id):
        images = PropertyImage.query.filter_by(property_id=property_id).all()
        schema = PropertyImageSchema(many=True)
        return success_response("Images fetched successfully", schema.dump(images))
