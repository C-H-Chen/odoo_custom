from odoo import fields, models

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ("check_name", "CHECK(price > 0)", "The price must be strictly positive"),    
    ]
    price = fields.Float("Price", required = True)
    validity = fields.Integer(string = "Validity (days)", default = 7)

    state = fields.Selection(    
        selection=[
            ("accepted", "Accepted"),
            ("refused", "refused"),
        
        ],
        string = "Status",
        required = True,
        copy = False,
        default = False,
    )

    # Relational
    partner_id = fields.Many2one("res.partner", string="Partner", required = True)
    property_id = fields.Many2one("estate.property", string="Property", required = True)
    property_type_id = fields.Many2one(
        "estate.property.type", related = "property_id.property_type_id", 
        string="Property offer", required = True)
