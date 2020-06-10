from scrapy.contrib.exporter import XmlItemExporter


class CustomXmlItemExporter(XmlItemExporter):
    def serialize_field(self, field, name, value):
        # Base XML exporter expects strings only. Convert any float or int to string.
        value = str(value)
        return super(CustomXmlItemExporter, self).serialize_field(field, name, value)
