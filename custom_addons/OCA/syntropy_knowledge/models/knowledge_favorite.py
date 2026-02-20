# Copyright 2026 Syntropy
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class KnowledgeFavorite(models.Model):
    """Favoritos personales de cada usuario."""

    _name = "knowledge.favorite"
    _description = "Knowledge Favorite"
    _order = "create_date desc"
    _rec_name = "article_id"

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Usuario",
        required=True,
        default=lambda self: self.env.user,
        index=True,
        ondelete="cascade",
    )
    article_id = fields.Many2one(
        comodel_name="knowledge.article",
        string="Artículo",
        required=True,
        index=True,
        ondelete="cascade",
    )
    notes = fields.Text(
        string="Notas personales",
        help="Notas privadas sobre este artículo",
    )

    _sql_constraints = [
        (
            "user_article_uniq",
            "UNIQUE(user_id, article_id)",
            "Este artículo ya está en tus favoritos.",
        ),
    ]
