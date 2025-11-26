STORE_SCHEMA = {
 "type": "object",
  "properties": {
    "id": {"type": "integer"},
    "petId": {"type": "integer"},
    "quantity": {"type": "number"},
    "shipDate": {"type": "string", "format": "date-time"},
    "status": {"type": "string"},
    "complete": {"type": "boolean"},
  },
  "required": ["id", "petId", "quantity", "shipDate", "status"],
  "additionalProperties": False
}

INVENTORY_SCHEMA = {
 "type": "object",
  "properties": {
    "approved": {"type": "integer"},
    "delivered": {"type": "integer"},
    "placed": {"type": "integer"},
  },
  "required": ["approved", "delivered"],
  "additionalProperties": False
}
