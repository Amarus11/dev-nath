# Copyright 2026 Syntropy
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class KnowledgeCategory(models.Model):
    """Categorías jerárquicas para organizar artículos de conocimiento."""

    _name = "knowledge.category"
    _description = "Knowledge Category"
    _parent_name = "parent_id"
    _parent_store = True
    _order = "sequence, name"

    name = fields.Char(
        string="Nombre",
        required=True,
        translate=True,
    )
    description = fields.Text(
        string="Descripción",
        translate=True,
    )
    sequence = fields.Integer(
        string="Secuencia",
        default=10,
    )
    active = fields.Boolean(
        string="Activo",
        default=True,
    )
    parent_id = fields.Many2one(
        comodel_name="knowledge.category",
        string="Categoría padre",
        index=True,
        ondelete="cascade",
    )
    parent_path = fields.Char(
        index=True,
        unaccent=False,
    )
    child_ids = fields.One2many(
        comodel_name="knowledge.category",
        inverse_name="parent_id",
        string="Subcategorías",
    )
    article_ids = fields.One2many(
        comodel_name="knowledge.article",
        inverse_name="category_id",
        string="Artículos",
    )
    article_count = fields.Integer(
        string="Nº Artículos",
        compute="_compute_article_count",
        store=True,
    )
    color = fields.Integer(
        string="Color",
        default=0,
    )
    icon = fields.Char(
        string="Icono",
        default="📁",
        help="Emoji o código de icono para representar la categoría",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Compañía",
        default=lambda self: self.env.company,
        index=True,
    )

    _sql_constraints = [
        (
            "name_parent_uniq",
            "UNIQUE(name, parent_id, company_id)",
            "Ya existe una categoría con ese nombre en el mismo nivel.",
        ),
    ]

    @api.depends("article_ids")
    def _compute_article_count(self):
        for category in self:
            category.article_count = len(category.article_ids)

    @api.constrains("parent_id")
    def _check_parent_recursion(self):
        if not self._check_recursion():
            raise models.ValidationError(
                self.env._("No se permiten categorías recursivas.")
            )

    def name_get(self):
        result = []
        for record in self:
            if record.parent_id:
                name = f"{record.parent_id.name} / {record.name}"
            else:
                name = record.name
            result.append((record.id, name))
        return result
