from mongoengine import Document,EmbeddedDocument, StringField, IntField, FloatField, EmbeddedDocumentField, BinaryField, BooleanField


class Productor(EmbeddedDocument):
    prod_id = IntField()
    prod_nombre= StringField()
    prod_apellido = StringField()
    prod_cod_gremio = IntField()
    prod_nombre_gremio = StringField()

class Categoria(EmbeddedDocument):
    cat_id = IntField()
    cat_nombre = StringField()
    
class Producto(Document):
    p_id = IntField(required=True,primary_key=True)
    p_nombre = StringField(required=True)
    categoria = EmbeddedDocumentField(Categoria)
    p_unidad = StringField(required=True)
    p_precio = FloatField(required=True)
    p_stock = IntField(required=True)
    productor = EmbeddedDocumentField(Productor)
    p_medicinal = BooleanField(required=True)
    imagen = BinaryField()