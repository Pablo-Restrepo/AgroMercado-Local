from mongoengine import Document,EmbeddedDocument, StringField, IntField, FloatField, EmbeddedDocumentField, ImageField


class Productor(EmbeddedDocument):
    prod_id = IntField()
    prod_nombre= StringField()
    prod_apellido = StringField()
    prod_cod_gremio = IntField()
    prod_nombre_gremio = StringField()

class Producto(Document):
    p_id = IntField(required=True,primary_key=True)
    p_nombre = StringField(required=True)
    p_tipo = StringField(required=True)
    p_unidad = StringField(required=True)
    p_precio = FloatField(required=True)
    dir_img = StringField(required=True)
    productor = EmbeddedDocumentField(Productor)
    imagen = ImageField(size=(271, 273, True), thumbnail_size=(271, 273, True))